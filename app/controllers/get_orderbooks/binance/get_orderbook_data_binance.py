import requests
import pandas as pd
from app.config.paths import data as path_to_data_folder
import os
from app.controllers.get_orderbooks.binance.format_binance_response_into_orderbook import format_binance_response_into_orderbook
from app.models.order_book.order_book import OrderBook
#import threading


def get_binance_orderbook_responses(exchange_currency_master: pd.DataFrame) -> dict[str, OrderBook]:
    #threading.Timer(100.0, get_kraken_orderbook_responses).start()
    #df = pd.read_csv(os.path.join(path_to_data_folder, 'xchange_curr_master.csv'))
    binance_instruments = exchange_currency_master[exchange_currency_master.xchg_code == 'Binance']['xchg_curr_pair'].unique().tolist()
    # print(bitstamp_instruments)
    binance_instruments = [instrument.upper() for instrument in binance_instruments]

    base_url = ' https://api.binance.com/api/v3'  # /Depth # ?pair=
    endpoint = '/depth'


    orderbooks: dict[str, OrderBook] = {}
    for instrument in binance_instruments:

        path_parameters = {
        "symbol": instrument,
        "limit": 1000
        }

        response = requests.get(url=base_url + endpoint, params=path_parameters)
        response=response.json() # resturns a dictionary or list
        #print(response)
        orderbooks[instrument] = format_binance_response_into_orderbook(response, instrument)
        if response == {'error': ['EQuery:Unknown asset pair']}:
            print(instrument, response)
        elif response == {'error': ['EQuery:Invalid asset pair']}:
            print(instrument, response)
        else:
            pass

    return orderbooks

if __name__ == "__main__":


    my_orderbook = get_binance_orderbook_responses()


