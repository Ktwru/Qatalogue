import django_filters
from .models import Car, Producer


class ProductFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter()
    year__gt = django_filters.NumberFilter(field_name='year', lookup_expr='gt')
    year__lt = django_filters.NumberFilter(field_name='year', lookup_expr='lt')

    producer = django_filters.ModelChoiceFilter(queryset=Producer.objects.all())

    class Meta:
        model = Car
        fields = ['year']
