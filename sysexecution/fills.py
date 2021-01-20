from collections import namedtuple

import pandas as pd

from syscore.objects import missing_order
from sysexecution.orders.base_orders import Order
from sysexecution.orders.list_of_orders import listOfOrders

Fill = namedtuple("Fill", ["date", "qty", "price"])


class listOfFills(list):
    def __init__(self, list_of_fills):
        list_of_fills = [
            fill for fill in list_of_fills if fill is not missing_order]
        super().__init__(list_of_fills)

    @classmethod
    def from_list_of_orders(listOfFills, list_of_orders: listOfOrders):
        order_list_as_fills = [fill_from_order(order) for order in list_of_orders]
        list_of_fills = listOfFills(order_list_as_fills)

        return list_of_fills

    def _as_dict_of_lists(self) -> dict:
        qty_list = [fill.qty for fill in self]
        price_list = [fill.price for fill in self]
        date_list = [fill.date for fill in self]

        return dict(qty=qty_list, price=price_list, date=date_list)

    def as_pd_df(self) -> pd.DataFrame:
        self_as_dict = self._as_dict_of_lists()
        date_index = self_as_dict.pop("date")
        df = pd.DataFrame(self_as_dict, index=date_index)
        df = df.sort_index()

        return df


def fill_from_order(order: Order) -> Fill:
    if order.fill_equals_zero():
        return missing_order

    fill_price = order.filled_price
    fill_datetime = order.fill_datetime
    fill_qty = order.fill

    if fill_price.is_empty():
        return missing_order

    if fill_datetime is None:
        return missing_order

    return Fill(fill_datetime, fill_qty, fill_price)