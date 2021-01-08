from abc import ABC


class OrderRepository(ABC):
    def __init__(self, data_source=[]):
        self.__data_source = data_source

    def find_by_id(self, order_id):
        return next((order for order in self.data_source if order.order_id == order_id), None)

    def add(self, order):
        if not self.find_by_id(order.order_id):
            self.__data_source.append(order)

    def delete(self, order):
        self.__data_source.remove(order)

    def update(self, order):
        self.delete(order)
        self.add(order)

    @property
    def data_source(self):
        return self.__data_source
