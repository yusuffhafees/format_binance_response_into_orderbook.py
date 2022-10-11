

import requests
import pandas as pd
from app.config.paths import data as path_to_data_folder
import os
from app.controllers.get_orderbooks.bitstamp.format_bitstamp_response_into_orderbook import format_bitstamp_response_into_orderbook
from app.models.order_book.order_book import OrderBook


def get_bitstamp_orderbook_responses(exchange_currency_master: pd.DataFrame) -> dict[str, OrderBook]:
    """

    :return:
    """
    #df = pd.read_csv(os.path.join(path_to_data_folder, 'xchange_curr_master.csv'))
    bitstamp_instruments = exchange_currency_master[exchange_currency_master.xchg_code == 'Bitstamp']['xchg_curr_pair'].unique().tolist()
    bitstamp_instruments = [instrument.replace("/", "").lower() for instrument in bitstamp_instruments]
    base_url = 'https://www.bitstamp.net/api/v2'  # /Depth # ?pair=
    endpoint = '/order_book'

    request_parameters = {
        'group': 1
    }

    orderbooks: dict[str, OrderBook] = {}

    for instrument in bitstamp_instruments:
        try:
            response = requests.get(url=base_url + endpoint + '/' + instrument, params=request_parameters)
            orderbooks[instrument] = format_bitstamp_response_into_orderbook(response.json(), instrument)
        except requests.exceptions.JSONDecodeError:
            print("++++++++JSON DECODE ERROR! \n")
            print(response, response.content, base_url + endpoint + '/' + instrument, request_parameters)
            print("++++++++JSON DECODE ERROR! \n")


    return orderbooks


if __name__ == "__main__":

    my_orderbook = get_bitstamp_orderbook_responses()
    print(my_orderbook)
    print("eof")