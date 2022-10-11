import pandas as pd

from app.controllers.analysis_updated.fast_spread import spread_amount
from app.controllers.get_orderbooks.load_orderbook import load_orderbooks
from app.models.order_book.order_book import OrderBook
from app.controllers.analysis_updated.get_cum_sum import include_cum_sum


def gradient(orderbook: OrderBook):
    print(f"\nStarting gradient calculation {orderbook.instrument}")
    spr, leg2_quant, equilibrum_quantity = spread_amount(orderbook)
    print("Calculating difference 1")
    spr['difference'] = spr[0].diff()
    print("Calculating difference 2")
    leg2_quant['difference'] = leg2_quant[0].diff()
    print("Calculating the raio")
    slopes = spr['difference'] / leg2_quant['difference']
    print("Calculating mean")
    mean_of_slopes = slopes.mean()
    # average_slope_of_coins.append(mean_of_slopes)
    print(f"Mean of the slopes is = {mean_of_slopes}")
    return mean_of_slopes


if __name__ == "__main__":
    average_slope_of_coins = []
    print("----- starting function ----- ")
    orderbook_list_names = ['ALICEEUR', '1INCHEUR', 'XXBTZEUR', 'XETHZEUR', 'OMGEUR', 'OXTEUR', 'PAXGEUR', 'POWREUR',
                            'QNTEUR', 'PERPEUR']
    list_orderbooks = load_orderbooks(orderbook_list_names)
    for my_orderbook in list_orderbooks:
        my_orderbook_improved = include_cum_sum(my_orderbook)
        average_slope_of_coins.append(gradient(my_orderbook_improved))

    print("----- ending function ----- ")

    orderbook_list_names = pd.DataFrame(orderbook_list_names)
    orderbook_list_names = orderbook_list_names.rename(columns={0: 'coinname'})
    average_slope_of_coins = pd.DataFrame(average_slope_of_coins)
    average_slope_of_coins = average_slope_of_coins.rename(columns={0: 'slope'})
    gradient_result = pd.concat([orderbook_list_names, average_slope_of_coins], axis=1)
    gradient_result['default_rank'] = gradient_result['slope'].rank()
    print(gradient_result)
