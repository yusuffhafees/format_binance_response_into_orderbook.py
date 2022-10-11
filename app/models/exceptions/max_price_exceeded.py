class MaxPriceExceeded(Exception):
    def __init__(self, quantity_remaining, bought_quantity,sold_quantity,price_executed):
        self.bought_quantity = bought_quantity
        self.quantity_remaining = quantity_remaining
        self.price_executed = price_executed
        self.sold_quantity = sold_quantity
