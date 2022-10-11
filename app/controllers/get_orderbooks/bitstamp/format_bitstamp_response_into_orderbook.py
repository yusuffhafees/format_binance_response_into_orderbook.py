import decimal

import pandas as pd
import datetime

from app.models.order_book.order_book import OrderBook, Order


def format_bitstamp_response_into_orderbook(bitstamp_response: dict, instrument) -> OrderBook:
    timestamp = datetime.datetime.fromtimestamp(int(bitstamp_response['timestamp']))  # unix time

    asks = [Order(instrument=instrument,
                  price=decimal.Decimal(price),
                  quantity=decimal.Decimal(quantity),
                  side='ask',
                  insertion_time=timestamp,
                  ) for price, quantity in bitstamp_response['asks']]

    bids = []
    for price, quantity in bitstamp_response['bids']:
        my_order = Order(price=decimal.Decimal(price),
                         quantity=quantity,
                         side='bid',
                         insertion_time=timestamp,
                         instrument=instrument)
        bids.append(my_order)

    return OrderBook(instrument=instrument,
                     bids=bids,
                     asks=asks)


