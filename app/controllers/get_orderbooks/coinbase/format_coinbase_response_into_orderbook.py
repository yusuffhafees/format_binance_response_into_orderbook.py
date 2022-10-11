import decimal
import datetime

from app.models.order_book.order_book import OrderBook, Order

def format_coinbase_response_into_orderbook(coinbase_response: dict, instrument) -> OrderBook:

    asks = [Order(instrument=instrument,
                  price=decimal.Decimal(price),
                  quantity=decimal.Decimal(quantity),
                  side='ask',
                  insertion_time=datetime.datetime.utcnow(),
                  ) for price, quantity, amount in coinbase_response['asks']]

    bids = []
    for price, quantity, amount in coinbase_response['bids']:
        my_order = Order(price=decimal.Decimal(price),
                         quantity=quantity,
                         side='bid',
                         insertion_time=datetime.datetime.utcnow(),
                         instrument=instrument)
        bids.append(my_order)

    return OrderBook(instrument=instrument,
                     bids=bids,
                     asks=asks)