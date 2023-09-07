from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase

from webapp.tests.factories.product import ProductFactory

User = get_user_model()


class TestCart(TestCase):
    def setUp(self):
        user, created = User.objects.get_or_create(username='user')
        if created:
            # admin.is_superuser = True
            user.set_password('user')
            user.save()
        self.client.login(username='user', password='user')
        self.product = ProductFactory.create(amount=4)
        user.user_permissions.add(Permission.objects.get(codename="add_product"))

    def test_add_cart_success(self):
        response = self.client.post(f"/product/{self.product.pk}/add-cart/", data={"qty": 2})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        session = self.client.session
        self.assertDictEqual(session.get("cart"), {str(self.product.pk): 2})

    def test_add_cart_existing_product_success(self):
        session = self.client.session
        session['cart'] = {str(self.product.pk): 2}
        session.save()

        response = self.client.post(f"/product/{self.product.pk}/add-cart/", data={"qty": 2})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        session = self.client.session
        self.assertDictEqual(session.get("cart"), {str(self.product.pk): 4})

    def test_add_cart_not_product_amount(self):
        response = self.client.post(f"/product/{self.product.pk}/add-cart/", data={"qty": 5})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_add_cart_not_product(self):
        self.product.delete()
        response = self.client.post(f"/product/1/add-cart/", data={"qty": 2})
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_test(self):
        with self.assertRaises(ZeroDivisionError):
            2 / 1
