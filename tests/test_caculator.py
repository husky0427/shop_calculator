import pytest
from caculator import Order, Caculator
from model import Product, User

book = Product('book', 100)
pen = Product('pen', 30)
notebook = Product('notebook', 50)

def test_order():
    danny = User('Danny')
    order = Order(danny)
    assert 'uuid' == order.order_id
    assert {} == order.commodities_in_order
    assert 0 == order.original_price

    order.add_commodity(book, 5)
    order.add_commodity(pen, 3)
    assert 'book' in [product.product_name for product in order.commodities_in_order.keys()]
    assert 'pen' in [product.product_name for product in order.commodities_in_order.keys()]

    expected_original_price = 590
    actual_original_price = order.original_price
    assert expected_original_price == actual_original_price


def test_caculator():
    john = User('John')
    order = Order(john)
    order.add_commodity(book, 5)
    order.add_commodity(pen, 3)

    caculator = Caculator(order)
    assert order.original_price == caculator.original_total_price
    assert [] == caculator.total_gifts

    