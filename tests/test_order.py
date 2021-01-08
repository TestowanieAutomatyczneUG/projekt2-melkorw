import unittest
from unittest.mock import *
from order.Order import Order
from order.OrderRepository import OrderRepository


# CLASS TESTES USING MOCK, SPY, STUB
class OrderTest(unittest.TestCase):

    def test_get_order_return_none(self):
        stub_repo = Mock(OrderRepository)
        order = Order(stub_repo)
        stub_repo.find_by_id.return_value = None
        response = order.get_order(1)
        self.assertEqual(response, 'Item does not exist')

    def test_get_order_return_order_exists(self):
        stub_repo = Mock(OrderRepository)
        order = Order(stub_repo)
        stub_repo.find_by_id.return_value = {'order': {'items': [{'name': 'name1', 'value': 10}, {'name': 'name2', 'value': 20}], 'order_id': 1, 'client_id': 1}}
        response = order.get_order(1)
        self.assertEqual(response['order']['order_id'], 1)

    def test_get_order_get_by_id_should_be_called(self):
        spy_repo = Mock(OrderRepository)
        order = Order(spy_repo)
        order.get_order(1)
        spy_repo.find_by_id.assert_has_calls([call(1), call(1)])
