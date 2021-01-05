import unittest
from order.order import Order


class OrderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = Order()

    def tearDown(self) -> None:
        self.temp = None
