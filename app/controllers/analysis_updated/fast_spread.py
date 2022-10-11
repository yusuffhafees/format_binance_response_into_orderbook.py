import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from app.controllers.get_orderbooks.bitfinex.load_orderbook import load_orderbooks
from app.models.order_book.order_book import OrderBook
from app.controllers.analysis_updated.fast_pricing import fast_pricing

number_of_datapoints = 1000


def spread_amount(orderbook: OrderBook, plotting: bool = False) -> tuple[pd.DataFrame, pd.DataFrame, float]:
    print(f"Calculating spread {orderbook.instrument}")
    # orderbook
    x = orderbook.bids
    y = orderbook.asks

    sum_of_bid_quantity = x['quantity'].sum()
    sum_of_ask_quantity = y['quantity'].sum()
    equilibrum_quantity = min(sum_of_bid_quantity, sum_of_ask_quantity)

    quant = []
    leg2_quant = []
    spr = []

    print(f"Starting to loop over: {number_of_datapoints}")
    for quantity_on_price in np.linspace(0, equilibrum_quantity, number_of_datapoints)[1:-1]:
        ask_price = fast_pricing(orderbook, quantity_on_price, 'asks')  #/quantity_on_price
        bid_price = fast_pricing(orderbook, quantity_on_price, 'bids') #/quantity_on_price
        our_spread = (ask_price - bid_price) / (
                (ask_price + bid_price) / 2)  # gives the spread of the quantity starting from 0.25
        quant.append(quantity_on_price)
        leg2_quant.append(quantity_on_price * ((ask_price + bid_price) / 2))
        spr.append(our_spread)

    spr = pd.DataFrame(spr)
    leg2_quant = pd.DataFrame(leg2_quant)

    if plotting:
        plt.figure(figsize=(20, 6))
        plt.plot(leg2_quant.values, spr.values)
        plt.ylabel('spread')
        plt.xlabel('quantity')
        plt.show()

    print("Done with Spread_amount")

    return spr, leg2_quant, equilibrum_quantity


if __name__ == "__main__":
    from app.controllers.analysis_updated.get_cum_sum import include_cum_sum
    my_orderbook = include_cum_sum(load_orderbooks('tBTCEUR'))
    spreads, leg_2, eq_quant = spread_amount(my_orderbook)
    print(f"my spreads are:\n{spreads}")
    print(f"\n\nmy leg2 is are:\n{leg_2}")
# if __name__ == "__main__":
