import factory
from factory.django import DjangoModelFactory

from webapp.models import Cart
from webapp.tests.factories.product import ProductFactory


class CartFactory(DjangoModelFactory):
    qty = factory.Faker("pyint", min_value=1, max_value=10)
    product = factory.SubFactory(ProductFactory)

    class Meta:
        model = Cart
