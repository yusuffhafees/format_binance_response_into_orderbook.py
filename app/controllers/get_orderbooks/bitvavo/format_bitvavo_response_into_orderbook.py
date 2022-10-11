import decimal
import datetime

from app.models.order_book.order_book import OrderBook, Order

def format_bitvavo_response_into_orderbook(bitvavo_response: dict, instrument) -> OrderBook:
    #timestamp = datetime.datetime.fromtimestamp(int(bitstamp_response['timestamp']))  # unix time

    asks = [Order(instrument=instrument,
                  price=decimal.Decimal(price),
                  quantity=decimal.Decimal(quantity),
                  side='ask',
                  insertion_time=datetime.datetime.utcnow(),
                  ) for price, quantity in bitvavo_response['asks']]

    bids = []
    for price, quantity in bitvavo_response['bids']:
        my_order = Order(price=decimal.Decimal(price),
                         quantity=quantity,
                         side='bid',
                         insertion_time=datetime.datetime.utcnow(),
                         instrument=instrument)
        bids.append(my_order)

    return OrderBook(instrument=instrument,
                     bids=bids,
                     asks=asks)