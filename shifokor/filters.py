import django_filters
from django_filters import FilterSet

from shifokor.models import Shifokorlar


class ShifokorFilter(FilterSet):
    created_at__lt = django_filters.DateFilter(field_name = 'created_up', lookup_expr='lt')
    created_at__gt = django_filters.DateFilter(field_name='created_up', lookup_expr='gt')
    biriktirilgan_muassasa = django_filters.CharFilter(field_name='biriktirilgan_muassasa', lookup_expr='icontains')


    class Meta:
        model = Shifokorlar
        fields = ['created_at', 'biriktirilgan_muassasa']

