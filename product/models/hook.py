from django.db import models
from django.utils.translation import gettext_lazy as _

from product.managers import SubscriberManager


class Subscriber(models.Model):
    class Event(models.IntegerChoices):
        PRODUCT_CREATED = 1, _('Product Created')
        PRODUCT_UPDATED = 2, _('Product Updated')
        PRODUCT_DELETED = 3, _('Product Deleted')

    event = models.IntegerField(choices=Event.choices, default=Event.PRODUCT_CREATED)
    url = models.URLField()
    objects = SubscriberManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event', 'url'], name='unique_url_for_an_event'),
        ]
