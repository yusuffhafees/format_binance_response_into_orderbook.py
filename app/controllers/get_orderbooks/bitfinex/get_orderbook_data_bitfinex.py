import os


import requests
from app.controllers.get_orderbooks.bitfinex.format_bitfinex_response_into_orderbook import \
    format_bitfinex_response_into_orderbook, seperate_bitfinex_response_into_bid_and_ask
from app.models.order_book.order_book import OrderBook
#from format_bitfinex_response_into_orderbook import seperate_bitfinex_response_into_bid_and_ask
import pandas as pd
from app.config.paths import data as path_to_data_folder


def get_bitfinex_orderbook_responses(exchange_currency_master: pd.DataFrame) -> dict[str:OrderBook]:  # list[str]) -> list[Any]:
    """

    :return:
    """
    #df = pd.read_csv(os.path.join(path_to_data_folder, 'xchange_curr_master.csv'))
    bitfinex_instruments = exchange_currency_master[exchange_currency_master.xchg_code == 'Bitfinex']['xchg_curr_pair'].unique().tolist()
    base_url = 'https://api-pub.bitfinex.com/v2'  # /Depth # ?pair=
    endpoint = '/book'

    #print(bitfinex_instruments)
    orderbooks = {}
    for instrument in bitfinex_instruments:

        specific_url_part = f"/{instrument}/P0"

        response = requests.get(url=base_url + endpoint + specific_url_part)
        response = response.json()
        try:
            a = 1.4 + response[0][0]
        except TypeError:
            print(response, instrument)
            continue
        except IndexError:
            print(response, instrument)
            continue

        updated_response=seperate_bitfinex_response_into_bid_and_ask(response)

        orderbooks[instrument]=(format_bitfinex_response_into_orderbook(updated_response, instrument))
        # print(orderbooks)
        # new_orderbook = dict(zip(bitfinex_instruments, orderbooks))

    return orderbooks


if __name__ == "__main__":

    orderbook_dict = get_bitfinex_orderbook_responses(pd.read_csv(os.path.join(path_to_data_folder, 'xchange_curr_master.csv')))
    print(orderbook_dict)

    #print(orderbook_dict)
    print("eof")

