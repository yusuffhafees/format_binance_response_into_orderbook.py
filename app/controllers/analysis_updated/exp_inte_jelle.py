import pandas as pd

from app.controllers.analysis_updated.fast_spread import spread_amount
from app.controllers.get_orderbooks.load_orderbook import load_orderbooks
from app.models.order_book.order_book import OrderBook
from app.controllers.analysis_updated.get_cum_sum import include_cum_sum
import math


def exp_inte(orderbook: OrderBook) -> float:
    """
    Function takes in an orderbook and will use the trapezoidal rule to integrate over the spread/quantity graph

    :param orderbook:
    :return: float of the integral result
    """
    spread_df, leg2_quant, equilibrum_quantity = spread_amount(orderbook)
    exp_integral_result = 0.0
    for x,y, j,t in zip(spread_df.values, spread_df.values[1:], leg2_quant.values,leg2_quant.values[1:]):
        exp_integral_result += ((math.exp(-x)+ math.exp(-y))/2) * (t-j)
        #print(t,j)
    return exp_integral_result


if __name__ == "__main__":
    list_of_integral_results = []
    print("----- starting function ----- ")
    orderbook_list_names = ['aaveeur', 'btceur']
    list_orderbooks = load_orderbooks(orderbook_list_names)
    for my_orderbook in list_orderbooks:
        my_orderbook_improved = include_cum_sum(my_orderbook)
        list_of_integral_results.append(exp_inte(my_orderbook))
    print("----- ending function ----- ")

    orderbook_list_names = pd.DataFrame(orderbook_list_names)
    orderbook_list_names = orderbook_list_names.rename(columns={0: 'coinname'})
    sum_of_exp = pd.DataFrame(list_of_integral_results)
    sum_of_exp = sum_of_exp.rename(columns={0: 'exp_result'})
    exp_integral_result_df = pd.concat([orderbook_list_names, sum_of_exp], axis=1)
    exp_integral_result_df['default_rank'] = exp_integral_result_df['exp_result'].rank(ascending=False)
    print(exp_integral_result_df)

