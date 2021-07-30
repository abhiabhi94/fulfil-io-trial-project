from django.db.models.query import QuerySet
import pytest

from product.models import Subscriber


@pytest.mark.django_db
def test_get_subscribers():
    subscriber = Subscriber.objects.create(url='http://example.com', event=Subscriber.Event.PRODUCT_DELETED)

    subscribers = Subscriber.objects.get_subscribers(event=Subscriber.Event.PRODUCT_DELETED.value)
    assert isinstance(subscribers, QuerySet)
    assert list(subscribers) == [subscriber]
