import os.path

import requests
import pandas as pd
import json
import decimal
import datetime

from app.models.order_book.order.order import Order
from app.models.order_book.order_book import OrderBook
from app.config.paths import data as path_to_data_folder


def print_response() -> list[dict]:
    df = pd.read_csv(os.path.join(path_to_data_folder, 'xchange_curr_master.csv'))
    df = df[df.xchg_code == 'Kraken']
    base_url = 'https://api.kraken.com/0/public'  # /Depth # ?pair=
    endpoint = '/Depth'

    alL_responses = []

    for x in df['xchg_curr_pair'].unique()[0:5]:
            x = x.replace("/", "")

            path_parameters = {
             "pair": x,
             "count": 5
                }

            response = requests.get(url=base_url + endpoint, params=path_parameters)
            response=response.json() # resturns a dictionary or list
            alL_responses.append(response)
            if response == {'error': ['EQuery:Unknown asset pair']}:
                print(x, response)
            elif response == {'error': ['EQuery:Invalid asset pair']}:
                print(x, response)
            else:
                print(response)
    return alL_responses

# print(json.dumps(response, indent=4))

def create_orderbook(responses) -> list[OrderBook]:
    my_order_books = []
    for response in responses:
        our_data = response['result']
        kraken_instrument = list(our_data.keys())[0]
        asks = [
            Order(
                instrument=kraken_instrument,
                side="ask",
                quantity=decimal.Decimal(ask[1]),
                price=decimal.Decimal(ask[0]),
                insertion_time=datetime.datetime.fromtimestamp(ask[2])
            ) for ask in response["result"][kraken_instrument]['asks']
        ]
        bids = [
            Order(
                instrument=kraken_instrument,
                side="bid",
                quantity=decimal.Decimal(bid[1]),
                price=decimal.Decimal(bid[0]),
                insertion_time=datetime.datetime.fromtimestamp(bid[2])
            ) for bid in response["result"][kraken_instrument]['bids']
        ]
        my_order_books.append(
            OrderBook(
                instrument=kraken_instrument,
                bids=bids,
                asks=asks
            )
        )
    return my_order_books
        #print(my_order_books[-1].asks)
        #print(my_order_books[-1].bids)

    #print(my_order_books[0].bids)
    #print(my_order_books[0].asks)

def generate_orderbook_list() -> list[OrderBook]:
    return create_orderbook(print_response())


if __name__ == "__main__":

    orderbooks = create_orderbook(print_response())
    print("END")
