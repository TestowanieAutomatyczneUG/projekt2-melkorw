from abc import ABC


class OrderModel(ABC):
    def __init__(self, order_id=None, client=None, items=None):
        self.__order_id = order_id
        self.__client = client
        self.__items = items

    @property
    def client(self):
        return self.__client

    @client.setter
    def client(self, value):
        self.__client = value

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value):
        self.__items = value

    @property
    def order_id(self):
        return self.__order_id

    @order_id.setter
    def order_id(self, value):
        self.__order_id = value

