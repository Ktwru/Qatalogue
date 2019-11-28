import django_filters
from .models import Car, Producer
from django.forms import CheckboxSelectMultiple
from django.db.models import Count, Min, Max


class CarFilter(django_filters.FilterSet):
    initial_values = Car.objects.select_related('cars_ads').prefetch_related('cars_ads__price',
                                                                             'year').aggregate(
        year_min=Min('year'),
        year_max=Max('year'),
        price_min=Min('cars_ads__price'),
        price_max=Max('cars_ads__price'))
    year = django_filters.RangeFilter(lookup_expr='exact', help_text=str(
        initial_values['year_min']) + ' - ' + str(initial_values['year_max']))
    drive = django_filters.MultipleChoiceFilter(choices=Car.CAR_DRIVE_CHOICES, label="Drive unit",
                                                widget=CheckboxSelectMultiple)
    cars_ads__price = django_filters.RangeFilter(lookup_expr='exact', help_text=str(
        initial_values['price_min']) + ' - ' + str(initial_values['price_max']))

    class Meta:
        model = Car
        fields = ['producer', 'year', 'type', 'volume', 'power', 'drive', 'cars_ads__price']
