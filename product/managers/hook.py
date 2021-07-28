from django.db import models


class SubscriberManager(models.Manager):
    def get_subscribers(self, event):
        return self.filter(event=event)
