import requests
from celery.utils.log import get_task_logger

from config import celery_app
from product.models import Product
from product.models import Subscriber


logger = get_task_logger(__name__)


@celery_app.task(bind=True)
def product_saved_webhook(self, event_id, instance_pk):
    event_label = str(Subscriber.Event(event_id).label)
    urls = Subscriber.objects.get_subscribers(event=event_id).values_list('url', flat=True)
    instance = Product.objects.get(pk=instance_pk)
    # ideally this should be done in a separate thread
    for url in urls:
        try:
            requests.post(url, json={'event': event_label, **instance.serialize()})
        except ConnectionRefusedError:
            pass


@celery_app.task(bind=True)
def product_deleted_webhook(self, event_id, instance_pk):
    event_label = str(Subscriber.Event(event_id).label)
    urls = Subscriber.objects.get_subscribers(event=event_id).values_list('url', flat=True)
    # ideally this should be done in a separate thread
    for url in urls:
        try:
            requests.post(url, json={'event': event_label, 'id': instance_pk})
        except ConnectionRefusedError:
            pass
