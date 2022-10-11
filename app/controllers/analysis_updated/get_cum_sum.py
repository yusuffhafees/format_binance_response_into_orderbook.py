from app.controllers.get_orderbooks.bitstamp.load_orderbook import get_single_orderbook
from app.models.order_book.order_book import OrderBook


def include_cum_sum(orderbook: OrderBook) -> OrderBook:
    orderbook.asks['cumsum_quantity'] = orderbook.asks['quantity'].cumsum()
    orderbook.bids['cumsum_quantity'] = orderbook.bids['quantity'].cumsum()

    orderbook.asks['total_price'] = orderbook.asks['quantity'] * orderbook.asks['price']
    orderbook.bids['total_price'] = orderbook.bids['quantity'] * orderbook.bids['price']

    orderbook.asks['cumsum_price'] = orderbook.asks['total_price'].cumsum()
    orderbook.bids['cumsum_price'] = orderbook.bids['total_price'].cumsum()

    return orderbook


if __name__ == "__main__":
    my_orderbook = get_single_orderbook('btceur')
    my_orderbook_extra = include_cum_sum(my_orderbook)