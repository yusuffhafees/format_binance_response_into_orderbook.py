import dataclasses
import datetime
import decimal


@dataclasses.dataclass
class Order:
    instrument: str
    side: str
    quantity: decimal.Decimal
    price: decimal.Decimal
    insertion_time: datetime.datetime # due to price time priority
