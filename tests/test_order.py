import unittest
from unittest.mock import *
from assertpy import *
from order.Order import Order
from order.OrderRepository import OrderRepository
from order.OrderModel import OrderModel


# CLASS TESTES USING MOCK, SPY, STUB
class OrderTest(unittest.TestCase):

    def setUp(self) -> None:
        self.model = OrderModel(1, 1, [{'name': 'name1', 'value': 2}])

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

    def test_get_order_type_error(self):
        order = Order()
        assert_that(order.get_order).raises(TypeError).when_called_with('id')

    def test_get_order_value_error(self):
        order = Order()
        assert_that(order.get_order).raises(ValueError).when_called_with(-1)

    def test_add_order_true(self):
        stub_repo = Mock(OrderRepository)
        order = Order(stub_repo)
        stub_repo.add.return_value = True
        response = order.add_order(self.model)
        self.assertTrue(response)

    def test_add_order_add_should_be_called(self):
        spy_repo = Mock(OrderRepository)
        order = Order(spy_repo)
        order.add_order(self.model)
        spy_repo.add.assert_called_once_with(self.model)

    def test_add_order_type_error(self):
        order = Order(OrderRepository)
        assert_that(order.add_order).raises(TypeError).when_called_with('Not order model')

    def test_update_order_not_existing(self):
        stub_repo = Mock(OrderRepository)
        order = Order(stub_repo)
        stub_repo.update.return_value = False
        response = order.update_order(1, self.model)
        self.assertFalse(response)

    def test_update_order_exists(self):
        stub_repo = Mock(OrderRepository)
        order = Order(stub_repo)
        stub_repo.update.return_value = True
        response = order.update_order(1, self.model)
        self.assertTrue(response)

    def test_update_order_mock_called(self):
        spy_repo = Mock(OrderRepository)
        order = Order(spy_repo)
        order.update_order(1, self.model)
        spy_repo.update.assert_called_once()

    def test_update_order_type_error(self):
        order = Order()
        assert_that(order.update_order).raises(TypeError).when_called_with(1, 'not order model')

    def test_update_order_value_error(self):
        order = Order()
        assert_that(order.update_order).raises(ValueError).when_called_with(-1, self.model)

    def test_delete_order_return_existing_order(self):
        stub_repo = Mock(OrderRepository)
        order = Order(stub_repo)
        stub_repo.find_by_id.return_value = self.model
        response = order.delete_order(1)
        self.assertTrue(response)

    def test_delete_order_return_not_existing_order(self):
        stub_repo = Mock(OrderRepository)
        order = Order(stub_repo)
        stub_repo.find_by_id.return_value = None
        response = order.delete_order(1)
        assert_that(response).is_false()

    def test_delete_order_mock_should_be_called(self):
        spy_repo = Mock(OrderRepository)
        order = Order(spy_repo)
        order.delete_order(1)
        spy_repo.delete.assert_called_once()
        spy_repo.find_by_id.assert_has_calls([call(1), call(1)])

    def test_delete_order_type_error(self):
        order = Order()
        assert_that(order.delete_order).raises(TypeError).when_called_with('id')

    def test_delete_order_value_error(self):
        order = Order()
        assert_that(order.delete_order).raises(ValueError).when_called_with(-1)

    def tearDown(self) -> None:
        self.model = None
