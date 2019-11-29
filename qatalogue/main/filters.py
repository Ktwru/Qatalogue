import django_filters
from .models import Car, Motorcycle, Scooter
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


class MotorcycleFilter(django_filters.FilterSet):
    initial_values = Motorcycle.objects.select_related('motorcycles_ads').prefetch_related('motorcycles_ads__price').aggregate(
        price_min=Min('motorcycles_ads__price'),
        price_max=Max('motorcycles_ads__price'))
    motorcycles_ads__price = django_filters.RangeFilter(lookup_expr='exact', help_text=str(
        initial_values['price_min']) + ' - ' + str(initial_values['price_max'])
    )
    cylinders = django_filters.MultipleChoiceFilter(choices=((1, 1), (2, 2), (4, 4)), label="Number of cylinders",
                                                    widget=CheckboxSelectMultiple)

    class Meta:
        model = Motorcycle
        fields = ['producer', 'type', 'cylinders', 'volume', 'power', 'motorcycles_ads__price']


class ScooterFilter(django_filters.FilterSet):
    initial_values = Scooter.objects.select_related('scooters_ads').prefetch_related('scooters_ads__price').aggregate(
        price_min=Min('scooters_ads__price'),
        price_max=Max('scooters_ads__price'))
    scooters_ads__price = django_filters.RangeFilter(lookup_expr='exacts', help_text=str(
        initial_values['price_min']) + ' - ' + str(initial_values['price_max'])
    )

    class Meta:
        model = Scooter
        fields = ['producer', 'max_speed', 'battery_capacity', 'power', 'scooters_ads__price']
