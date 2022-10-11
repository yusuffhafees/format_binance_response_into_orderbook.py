import requests
import pandas as pd
from app.config.paths import data as path_to_data_folder
from app.controllers.get_orderbooks.kraken.forrmat_kraken_response_into_orderbook import format_kraken_response_into_orderbook
import os


from app.models.order_book.order_book import OrderBook

#import threading


def get_kraken_orderbook_responses(exchange_currency_master: pd.DataFrame) -> dict[str:OrderBook]:
    #threading.Timer(100.0, get_kraken_orderbook_responses).start()
    #df = pd.read_csv(os.path.join(path_to_data_folder, 'xchange_curr_master.csv'))
    df = exchange_currency_master[exchange_currency_master.xchg_code == 'Kraken']
    base_url = 'https://api.kraken.com/0/public'  # /Depth # ?pair=
    endpoint = '/Depth'


    orderbooks = {}

    for instruments in df['xchg_curr_pair'].unique():
        instrument = instruments.replace("/", "")

        path_parameters = {
        "pair": instrument,
        "count": 500
        }

        response = requests.get(url=base_url + endpoint, params=path_parameters)
        response=response.json() # resturns a dictionary or list


        # if response == {'error': ['EQuery:Unknown asset pair']}:
        #     print(x, response)
        # elif response == {'error': ['EQuery:Invalid asset pair']}:
        #     print(x, response)
        # else:
        #     pass
        #     print(response)
        orderbooks[instrument]=format_kraken_response_into_orderbook(response, instrument)
    return orderbooks

#(get_kraken_orderbook_responses())

