from django import forms
from .models import Producer, Car, CarAd, MotorcycleAd, ScooterAd
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

