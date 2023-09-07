from http import HTTPStatus

from django.test import TestCase

from webapp.models import Product, Cart
from webapp.tests.factories.cart import CartFactory
from webapp.tests.factories.category import CategoryFactory
from webapp.tests.factories.product import ProductFactory


class TestCartModel(TestCase):
    products = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_get_full_total(self):
        products = ProductFactory.create_batch(2, price=100, amount=2)
        for product in products:
            CartFactory.create(qty=2, product=product)
        result = Cart.get_full_total()
        self.assertEqual(400, result)
