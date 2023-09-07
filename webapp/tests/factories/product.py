import factory
from factory.django import DjangoModelFactory

from webapp.models import Product
from webapp.tests.factories.category import CategoryFactory


class ProductFactory(DjangoModelFactory):
    title = factory.Sequence(lambda t: f"Title{t}")
    description = factory.Faker("paragraph", nb_sentences=5)
    amount = factory.Faker("pyint", min_value=1, max_value=10)
    price = factory.Faker("pyint", min_value=100, max_value=500)
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = Product
