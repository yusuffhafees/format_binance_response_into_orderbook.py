import pprint

import requests
import pandas as pd
from app.config.paths import data as path_to_data_folder
import os
from app.controllers.get_orderbooks.coinbase.format_coinbase_response_into_orderbook import format_coinbase_response_into_orderbook
from app.models.order_book.order_book import OrderBook


def get_coinbase_orderbook_responses(exchange_currency_master: pd.DataFrame) -> dict[str, OrderBook]:
    """

    :return:
    """
    #df = pd.read_csv(os.path.join(path_to_data_folder, 'xchange_curr_master.csv'))
    coinbase_instruments = exchange_currency_master[exchange_currency_master.xchg_code == 'Coinbase']['xchg_curr_pair'].unique().tolist()
    coinbase_instruments = [instrument.lower() for instrument in coinbase_instruments]
    base_url = 'https://api.exchange.coinbase.com/products'  # /Depth # ?pair=
    endpoint = 'book'

    request_parameters = {
        'level': 2
    }
    orderbooks: dict[str, OrderBook] = {}


    for instrument in coinbase_instruments:
        response = requests.get(url=base_url +'/'+ instrument +'/'+ endpoint , params=request_parameters)
        response = response.json()
        #print(response)
        orderbooks[instrument] = format_coinbase_response_into_orderbook(response, instrument)

        if response == {'error': ['EQuery:Unknown asset pair']}:
            print(instrument, response)
        elif response == {'error': ['EQuery:Invalid asset pair']}:
            print(instrument, response)
        else:
            pass



    return orderbooks


if __name__ == "__main__":

    my_orderbook = get_coinbase_orderbook_responses()
    print(my_orderbook)
#     print("eof")