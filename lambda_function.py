# from app.merging import merging
# from app.coin_mark_analysis import coin_mark_analysis
from app.controllers.get_orderbooks.save_orderbook import save_orderbooks
from app.controllers.get_orderbooks.binance.get_orderbook_data_binance import get_binance_orderbook_responses
from app.controllers.get_orderbooks.bitfinex.get_orderbook_data_bitfinex import get_bitfinex_orderbook_responses
from app.controllers.get_orderbooks.bitvavo.get_bitvavo_orderbook import get_bitvavo_orderbook_responses
from app.controllers.get_orderbooks.coinbase.get_coinbase_orderbook import get_coinbase_orderbook_responses
from app.controllers.get_orderbooks.bitstamp.get_orderbook_data_bitstamp import get_bitstamp_orderbook_responses
from app.controllers.get_orderbooks.kraken.get_orderbook_data import get_kraken_orderbook_responses
from app.controllers.s3console import save_report_in_s3
from app.tools.encoding_helper import file2str
from app.tools.bytewrite_to_s3 import bytewrite_to_s3
import io
import pandas as pd
import os
from app.config.paths import data as path_to_data_folder




def lambda_handler(event, context):
    """
    start = datetime.datetime.utcnow()
    file_like_object = io.StringIO()
    refresh_cmc_data = True
    results_of_calculation = save_kraken_orderbooks()
    results_of_calculation.to_csv(file_like_object)
    #print(file_like_object.getvalue())
    base64_encoded_file=file2str(file_like_object.getvalue().encode())
    send_email(filename='spread.csv',file=base64_encoded_file,address='H.Yusuff@Bankhaus-Scheich.de', subject='bitvavo orderbook')
    stop = datetime.datetime.utcnow()
    delta = stop - start
    print(f"This took {delta}")
    #print(results_of_calculation)
    """

    exchange_currency_master = pd.read_csv(os.path.join(path_to_data_folder, 'xchange_curr_master.csv'))
    try:
        my_orderbook_binance = get_binance_orderbook_responses(exchange_currency_master)
        save_orderbooks(my_orderbook_binance, parent_folder="binance")
    except Exception as e:
        print(f"{e.__class__.__qualname__} - Error {e}")
    #
    try:
        my_orderbook_bitvavo = get_bitvavo_orderbook_responses(exchange_currency_master)
        save_orderbooks(my_orderbook_bitvavo,parent_folder='bitvavo')
    except Exception as e:
        print(f"{e.__class__.__qualname__} - Error {e}")
    #
    try:
        my_orderbook_bitstamp = get_bitstamp_orderbook_responses(exchange_currency_master)
        save_orderbooks(my_orderbook_bitstamp,parent_folder='bitstamp')
    except Exception as e:
        print(f"{e.__class__.__qualname__} - Error {e}")
    #
    try:
        my_orderbook_coinbase = get_coinbase_orderbook_responses(exchange_currency_master)
        save_orderbooks(my_orderbook_coinbase,parent_folder='coinbase')
    except Exception as e:
        print(f"{e.__class__.__qualname__} - Error {e}")
    #
    try:
        orderbook_bitfinex = get_bitfinex_orderbook_responses(exchange_currency_master)
        save_orderbooks(orderbook_bitfinex,parent_folder='bitfinex')
    except Exception as e:
        print(f"{e.__class__.__qualname__} - Error {e}")

    try:
        orderbook_kraken = get_kraken_orderbook_responses(exchange_currency_master)
        save_orderbooks(orderbook_kraken, parent_folder='kraken')
    except Exception as e:
        print(f"{e.__class__.__qualname__} - Error {e}")

    print("eof")





if __name__ == '__main__':
    lambda_handler(None, None)
