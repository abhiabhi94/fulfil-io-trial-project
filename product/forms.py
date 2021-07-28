from django import forms

from product.models import Product
from product.models import Subscriber


class ProductImportForm(forms.Form):
    product_file = forms.FileField()


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'sku', 'description', 'is_active',)


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ('url', 'event',)
