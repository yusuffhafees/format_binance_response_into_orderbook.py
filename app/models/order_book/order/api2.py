import requests
import pandas as pd
import json
import decimal
import datetime

from app.models.order_book.order.order import Order
from app.models.order_book.order_book import OrderBook

df = pd.read_csv('xchange_curr_master.csv')
base_url = 'https://api.kraken.com/0/public' #/Depth # ?pair=
# for curr_pair in df['curr_pair']:
#     url = url+curr_pair
#     url = url[:-1]
#     print(url)
endpoint = '/Depth'
path_parameters = {
        "pair": "BTCEUR",
        "count": 5
 }

response = requests.get(url=base_url + endpoint, params=path_parameters)
#print(response)
#print(response.json()) # resturns a dictionary or list
#print(json.dumps(response.json(), indent=4))


my_order_books = []
for kraken_instrument in response.json()['result'].keys():
    asks = [
        Order(
            instrument=kraken_instrument,
            side="ask",
            quantity=decimal.Decimal(ask[1]),
            price=decimal.Decimal(ask[0]),
            insertion_time=datetime.datetime.fromtimestamp(ask[2])
        ) for ask in response.json()["result"][kraken_instrument]['asks']
    ]
    bids = [
        Order(
            instrument=kraken_instrument,
            side="bid",
            quantity=decimal.Decimal(bid[1]),
            price=decimal.Decimal(bid[0]),
            insertion_time=datetime.datetime.fromtimestamp(bid[2])
        ) for bid in response.json()["result"][kraken_instrument]['bids']
    ]
    my_order_books.append(
        OrderBook(
            instrument=kraken_instrument,
            bids=bids,
            asks=asks
        )
    )
    print(my_order_books[0].asks)
    print(my_order_books[0].bids)
