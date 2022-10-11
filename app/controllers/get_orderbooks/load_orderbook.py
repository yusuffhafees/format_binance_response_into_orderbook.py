import os.path
import pandas as pd
from typing import Union

from app.config.paths import data as path_to_data
from app.models.order_book.order_book import OrderBook
#os.path.join(path_to_data_folder, 'orderbooks', 'bitstamp')

def get_single_orderbook(instrument: str) -> OrderBook:
    asks = pd.read_csv(os.path.join(path_to_data, 'orderbooks', 'bitvavo', f'{instrument}_asks.csv')).drop(columns='Unnamed: 0')
    bids = pd.read_csv(os.path.join(path_to_data, 'orderbooks',  'bitvavo', f'{instrument}_bids.csv')).drop(columns='Unnamed: 0')
    orderbook = OrderBook(instrument=instrument, bids=[], asks=[])
    orderbook._bids = bids
    orderbook._asks = asks
    return orderbook


def load_orderbooks(instruments: Union[list, str]) -> list[OrderBook]:
    print(f"loading orderbooks for {instruments}")
    orderbooks = []
    if type(instruments) == list:
        for instrument in instruments:
            orderbooks.append(
                get_single_orderbook(instrument)
            )
    elif type(instruments) == str:
        orderbooks.append(get_single_orderbook(instruments))
    else:
        raise TypeError
    print(f"returning {len(orderbooks)} orderbooks")
    return orderbooks


if __name__ == "__main__":
    print(load_orderbooks('AAVE-EUR'))