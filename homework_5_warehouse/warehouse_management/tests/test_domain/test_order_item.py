from warehouse_management.domain.models import OrderItem, Order

def test_generate_order_items(order_items, bunch_of_items):
    expected_1 = bunch_of_items[0].get('product_name')
    expected_2 = bunch_of_items[1].get('product_name')
    expected_3 = bunch_of_items[2].get('product_name')

    actual_1 = order_items[0].product_name
    actual_2 = order_items[1].product_name
    actual_3 = order_items[2].product_name

    assert actual_1 == expected_1
    assert actual_2 == expected_2
    assert actual_3 == expected_3

def test_order_item_sub_totals(order_items, bunch_of_items):
    expected_1 = (bunch_of_items[0].get('quantity') * bunch_of_items[0].get('unit_price'))
    expected_2 = (bunch_of_items[1].get('quantity') * bunch_of_items[1].get('unit_price'))
    expected_3 = (bunch_of_items[2].get('quantity') * bunch_of_items[2].get('unit_price'))

    actual_1 = order_items[0].sub_total
    actual_2 = order_items[1].sub_total
    actual_3 = order_items[2].sub_total

    assert actual_1 == expected_1
    assert actual_2 == expected_2
    assert actual_3 == expected_3






