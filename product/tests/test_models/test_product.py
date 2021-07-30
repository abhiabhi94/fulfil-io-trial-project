import pytest


@pytest.mark.django_db
def test_get_absolute_url(product):
    assert str(product.get_absolute_url()) == f'/products/detail/{product.pk}/'


@pytest.mark.django_db
def test_serialize(product):
    assert product.serialize() == {
        'id': product.id,
        'name': 'test',
        'sku': 'test-product',
        'description': 'test product',
        'is_active': product.is_active,
        'created_at': str(product.created_at),
        'updated_at': str(product.updated_at),
        'url': str(product.get_absolute_url())
    }
