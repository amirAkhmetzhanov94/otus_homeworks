from decimal import Decimal

import pytest

from warehouse_management.domain.models import OrderItem, Order, OrderStatus


def test_generate_orders(bunch_of_items, order_items):
    order = Order(id=1, items=order_items)

    expected = order_items
    actual = order.items

    assert actual == expected

def test_total_amount_property(bunch_of_items, order_items):
    order = Order(id=1, items=order_items)

    order_items_total_amount = Decimal(0)

    for item in order_items:
        order_items_total_amount += item.sub_total


    print(order_items_total_amount)
    print(order.total_amount)

    expected = order_items_total_amount
    actual = order.total_amount

    assert actual == expected


def test_add_item(generate_random_item, order_items):
    order = Order(id=1, items=list(order_items))
    random_item = OrderItem(**generate_random_item)

    order.add_item(random_item)

    actual_sum = order.total_amount
    expected_sum = sum(item.sub_total for item in order_items) + random_item.sub_total

    print(order_items)
    print(order.items)

    assert random_item in order.items
    assert actual_sum == expected_sum
    assert len(order.items) == len(order_items) + 1

@pytest.mark.parametrize(
    "test_input, expected", [
    ]
)
def test_change_status(test_input, expected):
    ...