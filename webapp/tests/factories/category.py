import factory
from factory.django import DjangoModelFactory

from webapp.models import Category


class CategoryFactory(DjangoModelFactory):
    title = factory.Sequence(lambda t: f"Title{t}")

    class Meta:
        model = Category
