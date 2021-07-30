from unittest.mock import patch

import pytest

from product.models import Subscriber
from product.factories import ProductFactory


@pytest.mark.django_db
def test_product_creation(faker):
    with patch('product.signals.product_saved_webhook') as mocked_task:
        product = ProductFactory()

        mocked_task.delay.assert_called_with(event_id=Subscriber.Event.PRODUCT_CREATED.value, instance_pk=product.pk)

@pytest.mark.django_db
def test_product_updation(product):
    with patch('product.signals.product_saved_webhook') as mocked_task:
        product.is_active = False
        product.save(update_fields=['is_active'])

        mocked_task.delay.assert_called_with(event_id=Subscriber.Event.PRODUCT_UPDATED.value, instance_pk=product.pk)


@pytest.mark.django_db
def test_product_deletion(product):
    with patch('product.signals.product_deleted_webhook') as mocked_task:
        product_pk = product.pk
        product.delete()

        mocked_task.delay.assert_called_with(event_id=Subscriber.Event.PRODUCT_DELETED.value, instance_pk=product_pk)
