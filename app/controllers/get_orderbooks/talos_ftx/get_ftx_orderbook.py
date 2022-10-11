import ast
from websocket import create_connection
import datetime
import hmac
import hashlib
import base64
import json
import datetime
import decimal
from app.models.order_book.order_book import OrderBook, Order
from app.config.config import talos_api_key,talos_api_secret
import os

import pandas as pd
# from app.controllers.s3console import save_report_in_s3
from app.config.paths import data as path_to_data_folder


def get_ftx_orderbook():
    df = pd.read_csv(os.path.join(path_to_data_folder, 'xchange_curr_master.csv'))
    talos_instruments = df[df.xchg_code == 'Talos_All']['xchg_curr_pair'].unique().tolist()
    list_to_remove = ['LUNC-BRL', 'LUNC-EUR', 'USTC-EUR', 'MIOTA-EUR', 'XNO-EUR']
    final_list = list(set(talos_instruments) - set(list_to_remove))

    print(final_list)

    api_key = talos_api_key
    api_secret = talos_api_secret



    utc_now = datetime.datetime.utcnow()
    utc_datetime = utc_now.strftime("%Y-%m-%dT%H:%M:%S.000000Z")

    host = "tal-43.sandbox.talostrading.com" # tal-1.prod.talostrading.com, for example
    path = "/ws/v1"
    params = "\n".join([
    "GET",
    utc_datetime,
    host,
    path,
    ])
    hash = hmac.new(
        api_secret.encode('ascii'), params.encode('ascii'), hashlib.sha256)
    hash.hexdigest()
    signature = base64.urlsafe_b64encode(hash.digest()).decode()
    header = {
    "TALOS-KEY": api_key,
    "TALOS-SIGN": signature,
    "TALOS-TS": utc_datetime,

    }
    #talos_instruments = ['1INCH-EUR', 'AAVE-EUR', 'ADA-BRL', 'ADA-CAD', 'ADA-EUR', 'ALGO-EUR', 'ALICE-EUR', 'ALPHA-EUR', 'AMP-EUR', 'BTC-USD', 'LUNC-EUR']
    ws = create_connection("wss://" + host + path, header=header)
    ws.send(json.dumps(

        {

            "reqid": 5,

            "type": "subscribe",

            "streams":

                [

                    {

                        "name": "MarketDataSnapshot",

                        "Symbol": instruments,

                        "Markets": ["ftx"],

                        "SizeBuckets": ["1", "5", "10"]

                    }

                    for instruments in final_list]

        }

    )

    )
    while True:

        response = json.loads(ws.recv())


        if response['type'] == 'hello' or 'Message' in response['data'][0]['Markets']['ftx']:
            continue
        response=format_orderbook_response(response)
        print(response)











def format_orderbook_response(response):
    #print((response))
    timestamp = datetime.datetime.strptime(response['ts'], '%Y-%m-%dT%H:%M:%S.%fZ')
    instrument= response['data'][0]['Symbol']
    prices_for_ask = [p['Price'] for p in response['data'][0]['Offers']]
    #print(prices_for_ask)
    quantities_for_ask = [q['Size'] for q in response['data'][0]['Offers']]
    #print(quantities_for_ask)

    asks = [Order(instrument=instrument,
                  price=price,
                  quantity=quantity,
                  side='ask',
                  insertion_time=timestamp
                  ) for price, quantity in zip(prices_for_ask, quantities_for_ask)]

    prices_for_bids = [p['Price'] for p in response['data'][0]['Bids']]
    #print(prices_for_bids)
    quantities_for_bids = [q['Size'] for q in response['data'][0]['Bids']]
    #print(quantities_for_bids)

    bids = []
    for price, quantity in zip(prices_for_bids, quantities_for_bids):
        my_order = Order(price=price,
                         quantity=quantity,
                         side='bid',
                         insertion_time=timestamp,
                         instrument=instrument)
        bids.append(my_order)

    return OrderBook(instrument=instrument,
                     bids=bids,
                     asks=asks)

# if __name__=='__main__':
#     response = {'reqid': 5, 'type': 'MarketDataSnapshot', 'seq': 188, 'ts': '2022-09-15T08:18:02.416936Z', 'data': [
#         {'Symbol': 'ETH-EUR', 'DepthType': 'VWAP', 'LiquidityType': 'Indicative',
#          'ExchangeTime': '2022-09-15T08:18:02.408000Z', 'SystemTime': '2022-09-15T08:18:02.408629Z',
#          'Bids': [{'Price': '1623.8', 'VWAP': '1623.8', 'Size': '1.00000000'},
#                   {'Price': '1622.9', 'VWAP': '1623.6', 'Size': '5.00000000'},
#                   {'Price': '1622.0', 'VWAP': '1623.0', 'Size': '10.00000000'}],
#          'Offers': [{'Price': '1626.6', 'VWAP': '1626.6', 'Size': '1.00000000'},
#                     {'Price': '1626.6', 'VWAP': '1626.6', 'Size': '5.00000000'},
#                     {'Price': '1629.0', 'VWAP': '1627.2', 'Size': '10.00000000'}], 'Markets': {
#             'ftx': {'Status': 'Online', 'ExchangeTime': '2022-09-15T08:18:02.408000Z',
#                     'SystemTime': '2022-09-15T08:18:02.408629Z'}}}]}
#
#     format_orderbook_response(response=response)

if __name__ == '__main__':

    # df = pd.read_csv(os.path.join(path_to_data_folder, 'xchange_curr_master.csv'))
    # talos_instruments = df[df.xchg_code == 'Talos_All']['xchg_curr_pair'].unique().tolist()
    # list_to_remove = ['LUNC-BRL', 'LUNC-EUR', 'USTC-EUR', 'MIOTA-EUR', 'XNO-EUR']
    # final_list = list(set(talos_instruments) - set(list_to_remove))
    #
    # print(final_list)
    print(get_ftx_orderbook())

