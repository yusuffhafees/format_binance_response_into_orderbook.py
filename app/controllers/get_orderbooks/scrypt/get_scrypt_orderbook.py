import asyncio
import json
import websockets
import datetime
import decimal
from app.models.order_book.order_book import OrderBook, Order

import os

import pandas as pd
# from app.controllers.s3console import save_report_in_s3
from app.config.paths import data as path_to_data_folder
#import _strptime
from app.config.config import api_token


async def show_ticker(instrument):
    headers = {"x-token-id": api_token}

    async with websockets.connect('wss://otcapp-qa.tradias.de/otc/ws', extra_headers=headers) as websocket:
        print(f"start {instrument}")
        my_ticker_subscription = {
            "type": "subscribe",
            "channelname": "Scryptprices",
            "instrument": instrument
        }

        await websocket.send(json.dumps(my_ticker_subscription))

        while True:
            received_msg = json.loads(await websocket.recv())
            print(received_msg)
            if 'event' in received_msg.keys():
                print(f'finish {instrument}')
                return format_scrypt_message(received_msg, instrument)
                # return Orderbook


def format_scrypt_message(scrypt_response, instrument):
    timestamp = datetime.datetime.strptime(scrypt_response['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')  # unix time
    prices_for_ask = [d['price'] for d in scrypt_response['levels']['sell']]

    quantities_for_ask = [d['quantity'] for d in scrypt_response['levels']['sell']]

    asks = [Order(instrument=instrument,
                  price=price,
                  quantity=quantity,
                  side='ask',
                  insertion_time=timestamp
                  ) for price, quantity in zip(prices_for_ask, quantities_for_ask)]

    prices_for_bid = [d['price'] for d in scrypt_response['levels']['buy']]
    quantities_for_bid = [d['quantity'] for d in scrypt_response['levels']['buy']]

    bids = []
    for price, quantity in zip(prices_for_bid, quantities_for_bid):
        my_order = Order(price=price,
                         quantity=quantity,
                         side='bid',
                         insertion_time=timestamp,
                         instrument=instrument)
        bids.append(my_order)

    return OrderBook(instrument=instrument,
                     bids=bids,
                     asks=asks)


# if __name__ == '__main__':
#     example = {'event': 'Scrypt',
#              'success':true
#             'instrument': 'XLMCAD',
#                'levels': {'buy': [{'price': 0.13722, 'quantity': 100},
#                                   {'price': 0.13722, 'quantity': 28377.8559},
#                                   {'price': 0.13722, 'quantity': 56655.7118},
#                                   {'price': 0.13723, 'quantity': 84933.5677},
#                                   {'price': 0.13723, 'quantity': 113211.4235},
#                                   {'price': 0.13723, 'quantity': 141489.2794},
#                                   {'price': 0.13723, 'quantity': 169767.1353},
#                                   {'price': 0.13724, 'quantity': 198044.9912}],
#                           'sell': [{'price': 0.1371, 'quantity': 100},
#                                    {'price': 0.13709, 'quantity': 28377.8559},
#                                    {'price': 0.13709, 'quantity': 56655.7118},
#                                    {'price': 0.13709, 'quantity': 84933.5677},
#                                    {'price': 0.13709, 'quantity': 113211.4235},
#                                    {'price': 0.13708, 'quantity': 141489.2794},
#                                    {'price': 0.13708, 'quantity': 169767.1353},
#                                    {'price': 0.13708, 'quantity': 198044.9912}]},
#                'success': True,
#                'timestamp': '2022-09-01T12:17:39.243Z'}
#     print(format_b2c2_message(example, instrument='XLMCAD'))

if __name__ == "__main__":
    df = pd.read_csv(os.path.join(path_to_data_folder, 'xchange_curr_master.csv'))
    scrypt_instruments = df[df.xchg_code == 'Scrypt']['curr_pair'].unique().tolist()
    orderbooks = []
    for instrument in scrypt_instruments:
        orderbooks.append(asyncio.run(show_ticker(instrument)))
    print(orderbooks)

