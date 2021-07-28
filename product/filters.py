import django_filters

from product.models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    active = django_filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = Product
        fields = ('name', 'sku', 'description', 'active',)
