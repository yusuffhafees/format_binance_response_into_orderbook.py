import pandas as pd
from app.models.order_book.order.order import Order


class OrderBook:
    """
    Order Book for a single instrument.
    """

    def __init__(self, instrument: str, bids: list[Order], asks: list[Order]):
        self.instrument = instrument
        self._bids = pd.DataFrame(list(sorted(bids, key=lambda bid: bid.price, reverse=True)))
        self._asks = pd.DataFrame(list(sorted(asks, key=lambda ask: ask.price, reverse=False)))

    @property
    def bids(self):
        return self._bids

    @bids.setter
    def bids(self, bids: list[Order]):
        self._bids = pd.DataFrame(list(sorted(bids, key=lambda bid: bid.price, reverse=True)))

    @property
    def asks(self):
        return self._asks

    @asks.setter
    def asks(self, asks: list[Order]):
        self._asks = pd.DataFrame(list(sorted(asks, key=lambda ask: ask.price, reverse=False)))

    def new_bid(self):
        """
        Inserting a new bid limit order into the book.
        :return:
        """
        pass

    def remove_bid(self):
        """
        Remove an existing bid limit order from the book. This can happen when the order expires, gets cancelled or gets executed.
        :return:
        """
        pass

    def update_bid(self):
        """
        Update an existing bid limit order in the book.
        :return:
        """
        pass

    def new_ask(self):
        pass

    def remove_ask(self):
        pass

    def update_ask(self):
        pass

    def __repr__(self):
         concat_df = pd.concat([self._asks, self._bids])
         return concat_df.to_string()

    # def __repr__(self):
    #      self._asks
    #      return self._asks.to_string()
    #
    # def __repr__(self):
    #      self._bids
    #      return self._bids.to_string()