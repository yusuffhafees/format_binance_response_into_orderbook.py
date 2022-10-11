import datetime
import os
from app.controllers.get_orderbooks.talos_ftx.get_ftx_orderbook import get_ftx_orderbook

from app.controllers.s3console import save_report_in_s3
from app.models.order_book.order_book import OrderBook
import io
import pandas as pd
import asyncio
from app.config.paths import data as path_to_data_folder


def save_orderbooks(orderbooks: dict[str, OrderBook], parent_folder: str = ""):
    # orderbooks = get_coinbase_orderbook_responses(coinbase_instruments)
    timestamp = datetime.datetime.utcnow()
    timestamp_as_string = timestamp.strftime("%Y-%m-%dT%H_%M_%S_%fZ")

    path = os.path.join(path_to_data_folder, 'orderbooks')

    for instrument in orderbooks:
        orderbook = orderbooks[instrument]
        #file_like_object_bids = io.StringIO()
        #file_like_object_asks = io.StringIO()
        orderbook.asks.to_csv(os.path.join(path, f'{orderbook.instrument}_asks.csv'))
        #orderbook.asks.to_csv(file_like_object_asks)
        orderbook.bids.to_csv(os.path.join(path, f'{orderbook.instrument}_bids.csv'))
        #orderbook.bids.to_csv(file_like_object_bids)

        if parent_folder:
            path = f"{parent_folder}/{orderbook.instrument}/{timestamp_as_string}"
        else:
            path = f"{orderbook.instrument}/{timestamp_as_string}"
        file_path_bid = f"{path}/bids.csv"
        #save_report_in_s3(file_like_object_bids, file_path_bid)
        file_path_ask = f"{path}/asks.csv"
        #save_report_in_s3(file_like_object_asks, file_path_ask)


if __name__ == "__main__":
    my_orderbook = get_ftx_orderbook()
    save_orderbooks(my_orderbook)
    print("eof")
