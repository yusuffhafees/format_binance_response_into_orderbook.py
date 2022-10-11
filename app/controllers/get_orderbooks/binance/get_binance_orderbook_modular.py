import requests
import pandas as pd
from app.config.paths import data as path_to_data_folder
import os
from app.controllers.get_orderbooks.binance.format_binance_response_into_orderbook import \
    format_binance_response_into_orderbook
from app.models.order_book.order_book import OrderBook


# import threading


def get_binance_orderbook_responses(instrument: str) -> OrderBook:
    base_url = ' https://api.binance.com/api/v3'  # /Depth # ?pair=
    endpoint = '/depth'

    path_parameters = {
        "symbol": instrument,
        "limit": 1000
    }
    response = requests.get(url=base_url + endpoint, params=path_parameters).json()
    print(response)
    return format_binance_response_into_orderbook(response, instrument)


if __name__ == "__main__":
    my_orderbook = get_binance_orderbook_responses('LUNABRL')
