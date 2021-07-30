from unittest.mock import patch

import pytest
from django.db.models.query import QuerySet

from product.models import Subscriber
from product.tasks import product_saved_webhook
from product.tasks import product_deleted_webhook

@pytest.fixture(scope='function')
def mocked_urls(monkeypatch):
    class MockQuerySet:
        def __init__(self, *args, **kwargs):
            pass

        def values_list(self, *args, **kwargs):
            return ['http://example.com', 'https://www.example.com',]

    monkeypatch.setattr('product.tasks.hook.Subscriber.objects.get_subscribers', MockQuerySet)


@pytest.mark.django_db
def test_product_saved_webhook_when_created(product, subscriber, mocked_urls):
    with patch('product.tasks.hook.requests') as mocked_requests:
        product_saved_webhook(event_id=Subscriber.Event.PRODUCT_CREATED.value, instance_pk=product.pk)

        assert mocked_requests.called_with(
            subscriber.url,
            json={'event': Subscriber.Event.PRODUCT_CREATED.label, **product.serialize()}
        )


@pytest.mark.django_db
def test_product_saved_webhook_when_updated(product, subscriber, mocked_urls):
    with patch('product.tasks.hook.requests') as mocked_requests:
        product_saved_webhook(event_id=Subscriber.Event.PRODUCT_UPDATED.value, instance_pk=product.pk)

        assert mocked_requests.called_with(
            subscriber.url,
            json={'event': Subscriber.Event.PRODUCT_UPDATED.label, **product.serialize()}
        )


@pytest.mark.django_db
def test_product_saved_webhook_when_cant_connect_to_subscriber_url(product, subscriber, mocked_urls):
    with patch('product.tasks.hook.requests.post', side_effect=ConnectionError()) as mocked_requests:
        with pytest.raises(ConnectionError):
            product_saved_webhook(event_id=Subscriber.Event.PRODUCT_UPDATED.value, instance_pk=product.pk)


@pytest.mark.django_db
def test_product_deleted_webhook(product, subscriber, mocked_urls):
    with patch('product.tasks.hook.requests') as mocked_requests:
        product_deleted_webhook(event_id=Subscriber.Event.PRODUCT_DELETED.value, instance_pk=product.pk)

        assert mocked_requests.called_with(
            subscriber.url,
            json={'event': Subscriber.Event.PRODUCT_DELETED.label, 'id': product.pk}
        )


@pytest.mark.django_db
def test_product_deleted_webhook_when_cant_connect_to_subscriber_url(product, subscriber, mocked_urls):
    with patch('product.tasks.hook.requests.post', side_effect=ConnectionError()) as mocked_requests:
        with pytest.raises(ConnectionError):
            product_deleted_webhook(event_id=Subscriber.Event.PRODUCT_UPDATED.value, instance_pk=product.pk)
