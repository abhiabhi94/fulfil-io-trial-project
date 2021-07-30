import factory

from product.models import Product
from product.models import Subscriber


class ProductFactory(factory.django.DjangoModelFactory):
    name = 'test'
    sku = 'test-product'
    description = 'test product'

    class Meta:
        model = Product
        django_get_or_create = ('sku', )


class SubscriberFactory(factory.django.DjangoModelFactory):
    url = 'https://example.com'

    class Meta:
        model = Subscriber
        django_get_or_create = ('url',)
