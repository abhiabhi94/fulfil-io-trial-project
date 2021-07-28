import django_tables2 as tables
from django.urls import reverse_lazy
from django.utils.html import format_html

from product.models import Product


class ProductTable(tables.Table):
    is_active = tables.Column(verbose_name='Active')

    class Meta:
        model = Product
        fields = ('name', 'sku', 'description', 'is_active',)

    def render_name(self, value, record):
        url = reverse_lazy('product:detail', args=[record.pk])
        return format_html('<a href="{}" title="{}">{}</a>', url, value, value)
