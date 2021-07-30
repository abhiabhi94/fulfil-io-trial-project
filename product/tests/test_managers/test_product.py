import pytest

from product.models import Product
from product.factories import ProductFactory


@pytest.mark.django_db
def test_bulk_upsert(django_assert_num_queries):
    products = [Product(name=str(i), sku=f'sku-{i}', description=f'des {i}') for i in range(100)]
    with django_assert_num_queries(1):
        Product.objects.bulk_upsert(products, keys=['sku'])

    # test with updation
    with django_assert_num_queries(1):
        Product.objects.bulk_upsert(products, keys=['sku'])


def test_bulk_upsert_without_keys():
    with pytest.raises(AssertionError) as exc:
        Product.objects.bulk_upsert([Product(name='t', description='t', sku='t')])

    assert str(exc.value) == 'Empty key fields'


def test_bulk_upsert_without_objects():
   assert Product.objects.bulk_upsert([], keys=['sku']) is None


@pytest.mark.django_db
def test_delete_all(django_assert_num_queries):
    products = [Product(name=str(i), sku=f'sku-{i}', description=f'des {i}') for i in range(100)]
    Product.objects.bulk_upsert(products, keys=['sku'])

    with django_assert_num_queries(1):
        Product.objects.delete_all()
