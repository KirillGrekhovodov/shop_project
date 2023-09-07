from http import HTTPStatus

from django.test import TestCase

from webapp.models import Product
from webapp.tests.factories.category import CategoryFactory
from webapp.tests.factories.product import ProductFactory


class TestProduct(TestCase):
    category = None
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = CategoryFactory.create()
        cls.correct_data = {
            "title": "test",
            "description": "test_description",
            "amount": 1,
            "price": 100,
            "category": cls.category.id
        }

    @classmethod
    def tearDownClass(cls):
        pass

    def test_create_product(self):
        response = self.client.post("/products/add/", data=self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().title, self.correct_data['title'])


    def test_create_product_no_category(self):
        data = {
            "title": "test",
            "description": "test_description",
            "amount": 1,
            "price": 100,
        }
        self.client.post("/products/add/", data=data)
        # self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(Product.objects.count(), 0)

    def test_update_product(self):
        product = ProductFactory.create(title="update_product")
        response = self.client.post(f"/product/{product.id}/update/", data=self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        print(Product.objects.count())
        self.assertEqual(Product.objects.first().title, self.correct_data['title'])
