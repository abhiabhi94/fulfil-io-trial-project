import pytest


from product.factories import ProductFactory, SubscriberFactory


@pytest.fixture
def product():
    return ProductFactory()


@pytest.fixture
def subscriber():
    return SubscriberFactory()
