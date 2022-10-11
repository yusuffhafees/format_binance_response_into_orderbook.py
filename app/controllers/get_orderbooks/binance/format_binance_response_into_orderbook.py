import decimal
import datetime

from app.models.order_book.order_book import OrderBook, Order

def format_binance_response_into_orderbook(binance_response: dict, instrument) -> OrderBook:
    #timestamp = datetime.datetime.fromtimestamp(int(bitstamp_response['timestamp']))  # unix time



    bids = []
    for price, quantity in binance_response['bids']:
        my_order = Order(price=decimal.Decimal(price),
                         quantity=quantity,
                         side='bid',
                         insertion_time=datetime.datetime.utcnow(),
                         instrument=instrument)
        bids.append(my_order)
    asks = [Order(instrument=instrument,
                  price=decimal.Decimal(price),
                  quantity=decimal.Decimal(quantity),
                  side='ask',
                  insertion_time=datetime.datetime.utcnow(),
                  ) for price, quantity in binance_response['asks']]
    return OrderBook(instrument=instrument,
                     bids=bids,
                     asks=asks)