import pandas as pd

from app.controllers.analysis_updated.get_cum_sum import include_cum_sum
from app.controllers.get_orderbooks.bitfinex.load_orderbook import get_single_orderbook
from app.models.order_book.order_book import OrderBook


def fast_pricing(orderbook: OrderBook, quantity, order_type: str) -> float:
    """
    Calculate the price of desired quantity in a given orderbook.

    :param orderbook:
    :param quantity: desired quantity
    :param order_type: Can be either 'buy' or 'sell'
    :return: price at which you can buy the desired quantity
    """

    book_side: pd.DataFrame = getattr(orderbook, order_type)
    index = (book_side['cumsum_quantity'] - quantity).apply(abs).idxmin()
    if index == 0:
        total_price = book_side.iloc[index]['price'] * quantity
    else:
        total_price = book_side.iloc[index - 1]['cumsum_price']
        remaining_quantity = quantity - book_side.iloc[index - 1]['cumsum_quantity']
        total_price += book_side.iloc[index]['price'] * remaining_quantity

    return total_price/quantity


if __name__ == "__main__":
    imporved_btc_book = include_cum_sum(get_single_orderbook('tBTCEUR')[0])
    print(fast_pricing(imporved_btc_book, 20, 'asks'))
