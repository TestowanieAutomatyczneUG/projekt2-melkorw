from abc import ABC


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

    def get_order_item(self, order_id, item_id):
        pass