from django import forms
from .models import Producer, Car
from django.db.models import Count, Min, Max


class RegistrationUser(forms.Form):
    username = forms.CharField(label="Username")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput, min_length=8)
    email = forms.EmailField(label="Email")
    dealer = forms.BooleanField(label="Dealer", required=False)


class RegistrationDealer(forms.Form):
    website = forms.URLField(label="Website")
    description = forms.CharField(label="Description", widget=forms.Textarea)


class SetCars(forms.Form):
    initial_values = Car.objects.select_related('cars_ads').prefetch_related('cars_ads__price',
                                                                            'year').aggregate(
        year_min_initial=Min('year'),
        year_max_initial=Max('year'),
        price_min_initial=Min('cars_ads__price'),
        price_max_initial=Max('cars_ads__price'))

    #producer = forms.ModelChoiceField(label="Producer", required=False, queryset=Producer)
    year_min = forms.IntegerField(label="Older than", required=False, initial=initial_values['year_min_initial'])
    year_max = forms.IntegerField(label="Younger than", required=False, initial=initial_values['year_max_initial'])
    type = forms.ChoiceField(label="Type", required=False, choices=Car.CAR_TYPE_CHOICES)
    volume = forms.IntegerField(label="Volume", required=False)
    power = forms.IntegerField(label="Power", required=False)
    drive = forms.MultipleChoiceField(label="Drive unit", required=False, choices=Car.CAR_DRIVE_CHOICES,
                                      widget=forms.CheckboxSelectMultiple)
    price_min = forms.IntegerField(label="More expensive than", required=False, initial=initial_values['price_min_initial'])
    price_max = forms.IntegerField(label="Cheaper than", required=False, initial=initial_values['price_max_initial'])
    has_ads = forms.BooleanField(label="Has ads now", required=False)
