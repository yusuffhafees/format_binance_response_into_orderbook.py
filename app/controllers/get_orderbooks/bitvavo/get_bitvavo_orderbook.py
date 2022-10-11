from python_bitvavo_api.bitvavo import Bitvavo
import requests
import pandas as pd
from app.config.paths import data as path_to_data_folder
import os
from app.controllers.get_orderbooks.bitvavo.format_bitvavo_response_into_orderbook import format_bitvavo_response_into_orderbook
from app.models.order_book.order_book import OrderBook


def get_bitvavo_orderbook_responses(exchange_currency_master: pd.DataFrame) -> dict[str, OrderBook]:
    #df = pd.read_csv(os.path.join(path_to_data_folder, 'xchange_curr_master.csv'))
    bitvavo_instruments = exchange_currency_master[exchange_currency_master.xchg_code == 'BitVavo']['xchg_curr_pair'].unique().tolist()
    # print(bitstamp_instruments)
    bitvavo_instruments = [instrument for instrument in bitvavo_instruments]
    print(bitvavo_instruments)


    orderbooks: dict[str, OrderBook] = {}
    for instrument in bitvavo_instruments:
        bitvavo = Bitvavo()
        response = bitvavo.book(instrument, {})
    #print(response)
        orderbooks[instrument] = format_bitvavo_response_into_orderbook(response, instrument)

    return orderbooks



import pprint





if __name__ == "__main__":

    my_orderbook = get_bitvavo_orderbook_responses()
    print(my_orderbook)
#     print("eof")