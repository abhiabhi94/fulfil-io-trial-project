from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

from product.models import Product
from product.models import Subscriber
from product.tasks import product_deleted_webhook
from product.tasks import product_saved_webhook


__all__ = ('product_saved', 'product_deleted',)


@receiver(post_save, sender=Product)
def product_saved(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        product_saved_webhook.delay(event_id=Subscriber.Event.PRODUCT_CREATED.value, instance_pk=instance.pk)
    else:
        product_saved_webhook.delay(event_id=Subscriber.Event.PRODUCT_UPDATED.value, instance_pk=instance.pk)


@receiver(post_delete, sender=Product)
def product_deleted(sender, instance, using, **kwargs):
    product_deleted_webhook.delay(event_id=Subscriber.Event.PRODUCT_DELETED.value, instance_pk=instance.pk)
