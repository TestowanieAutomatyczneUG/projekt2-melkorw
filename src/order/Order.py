from abc import ABC
from order.OrderModel import OrderModel

class Order(ABC):
    def __init__(self, order_repository=None):
        self.fake_api = 'https://virtual-shop.pl/api/orders'
        self.order_repository = order_repository

    def get_order(self, order_id):
        if type(order_id) is not int:
            raise TypeError('Order id must be integer')
        if order_id < 0:
            raise ValueError('Order id must be greater or equal 0')
        if self.order_repository.find_by_id(order_id):
            return self.order_repository.find_by_id(order_id)
        else:
            return 'Item does not exist'

    def add_order(self, order):
        if isinstance(order, OrderModel) is False:
            raise TypeError('Order is not OrderModel type')
        return self.order_repository.add(order)

    def update_order(self, order_id, new_order):
        if type(order_id) is not int or isinstance(new_order, OrderModel) is False:
            raise TypeError('Order is not OrderModel type or order id is not int')
        if order_id < 0:
            raise ValueError('Order id must be greater or equal 0')
        return self.order_repository.update(order_id, new_order)

    def delete_order(self, order_id):
        if type(order_id) is not int:
            raise TypeError('Order id is not integer')
        if order_id < 0:
            raise ValueError('Order is must be greater or equal 0')
        if self.order_repository.find_by_id(order_id):
            self.order_repository.delete(self.order_repository.find_by_id(order_id))
            return True
        return False
