import decimal
import datetime

from app.models.order_book.order_book import OrderBook, Order


def seperate_bitfinex_response_into_bid_and_ask(response: list) -> dict:
    output_dict = {
        'asks': [],
        'bids': []
    }
    for each_response in response:
        if each_response[2] < 0:
            output_dict['asks'].append((each_response[0], each_response[1] * each_response[2]))
        else:
            output_dict['bids'].append((each_response[0], each_response[1] * each_response[2]))

    return output_dict


def format_bitfinex_response_into_orderbook(bitfinex_response: dict, instrument: str) -> OrderBook:
    # timestamp = datetime.datetime.fromtimestamp(int(bitstamp_response['timestamp']))  # unix time

    asks = []
    for price, quantity in bitfinex_response['asks']:
        asks.append(Order(instrument=instrument,
                          price=decimal.Decimal(price),
                          quantity=decimal.Decimal(quantity),
                          side='ask',
                          insertion_time=datetime.datetime.utcnow(),
                          ))

    bids = []
    for price, quantity in bitfinex_response['bids']:
        my_order = Order(price=decimal.Decimal(price),
                         quantity=quantity,
                         side='bid',
                         insertion_time=datetime.datetime.utcnow(),
                         instrument=instrument)
        bids.append(my_order)

    return OrderBook(instrument=instrument,
                     bids=bids,
                     asks=asks)


if __name__ == '__main__':
    example_response = [[20235, 5, 0.91540815],
                        [20234, 5, 1.78986739],
                        [20233, 3, 0.91644492],
                        [20232, 3, 0.95499936],
                        [20230, 1, 0.3],
                        [20229, 2, 0.45536052],
                        [20228, 9, 6.34035727],
                        [20227, 6, 2.24567684],
                        [20226, 4, 1.01722984],
                        [20224, 2, 0.373748],
                        [20223, 2, 0.50546736],
                        [20222, 4, 0.52900266],
                        [20221, 4, 1.70600334],
                        [20220, 2, 1.56039593],
                        [20219, 1, 0.123767],
                        [20218, 3, 0.50400851],
                        [20217, 8, 1.41165735],
                        [20216, 1, 0.001],
                        [20215, 3, 4.956737],
                        [20214, 4, 0.12626137],
                        [20213, 4, 2.37851849],
                        [20212, 2, 15.584],
                        [20211, 4, 0.6238],
                        [20210, 3, 0.22381656],
                        [20209, 3, 0.24860301],
                        [20236, 1, -15],
                        [20237, 2, -0.173678],
                        [20238, 3, -0.47357736],
                        [20240, 2, -0.247317],
                        [20241, 3, -1.11276303],
                        [20242, 1, -0.5721],
                        [20243, 3, -0.49661602],
                        [20244, 2, -1.2882],
                        [20245, 2, -0.3984],
                        [20246, 1, -0.08311509],
                        [20247, 1, -0.5207],
                        [20248, 4, -2.01829403],
                        [20250, 4, -0.644757],
                        [20251, 4, -1.00658417],
                        [20252, 4, -2.393605],
                        [20253, 2, -0.32645497],
                        [20254, 4, -1.82549249],
                        [20255, 5, -0.28781177],
                        [20256, 3, -0.10058743],
                        [20257, 5, -2.07030345],
                        [20258, 1, -2.472246],
                        [20260, 1, -0.14690017],
                        [20261, 2, -3.331],
                        [20262, 2, -1.89385787],
                        [20263, 2, -0.95487587]]
    seperated_bitfinex_response = seperate_bitfinex_response_into_bid_and_ask(example_response)
    orderbook_of_bitstamp = format_bitfinex_response_into_orderbook(seperated_bitfinex_response, instrument='btceur')
    print(type(orderbook_of_bitstamp))
    #
    #
    # print(seperate_bitfinex_response_into_bid_and_ask(example_response))
    # output_dict = seperate_bitfinex_response_into_bid_and_ask(example_response)
    # orderbooks = format_bitfinex_response_into_orderbook(output_dict)
    # print(orderbooks)
    # # for x in orderbooks:
    # #     bitfinex_response = seperate_bitfinex_response_into_bid_and_ask(x)
    # #     print(format_bitfinex_response_into_orderbook(bitfinex_response, instrument= 'tBTCEUR'))


# def seperated_bitfinex_response_into_bid_and_ask():
#     return None