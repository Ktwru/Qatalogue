from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponsePermanentRedirect
from main.models import *
from django.db.models import Count, Min, Value, CharField
from itertools import chain
from .forms import RegistrationUser, RegistrationDealer, SetCars
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist


def main_paige(request):
    return render(request, "main_page.html")


def ads(request, category):
    if category == 'cars':
        product = Car.objects.select_related('cars_ads').prefetch_related('cars_ads__price').annotate(
            ads=Count('cars_ads'), min=Min('cars_ads__price')).all().values_list('producer__name', 'model', 'id',
                                                                                 'min', 'ads')
        category_name = 'Cars'
        filter_form = SetCars
    elif category == 'motorcycles':
        product = Motorcycle.objects.select_related('motorcycles_ads').prefetch_related(
            'motorcycles_ads__price').annotate(
            ads=Count('motorcycles_ads'), min=Min('motorcycles_ads__price')).all().values_list('producer__name',
                                                                                               'model', 'id',
                                                                                               'min', 'ads')
        category_name = 'Motorcycles'
    elif category == 'scooters':
        product = Scooter.objects.select_related('scooters_ads').prefetch_related('scooters_ads__price').annotate(
            ads=Count('scooters_ads'), min=Min('scooters_ads__price')).all().values_list('producer__name', 'model',
                                                                                         'id',
                                                                                         'min', 'ads')
        category_name = 'Scooters'
    else:
        return HttpResponseBadRequest("<h1>Bad Request</h1>")
    return render(request, "ads.html", {"products": product, "category_name": category_name,
                                        "category": category, "filter_form": filter_form})


def ad(request, category, id):
    if category == 'cars':
        product = Car.objects.get(id=id)
        ads = CarAd.objects.filter(product=product)
    elif category == 'motorcycles':
        product = Motorcycle.objects.get(id=id)
        ads = MotorcycleAd.objects.filter(product=product)
    elif category == 'scooters':
        product = Scooter.objects.get(id=id)
        ads = ScooterAd.objects.filter(product=product)
    else:
        return HttpResponseBadRequest("<h1>Bad Request</h1>")
    return render(request, "ad.html", {"product": product, "ads": ads, "category": category})


def dealers(request):
    dealer = Dealer.objects.annotate(
        ads=Count('scooters_ads') + Count('cars_ads') + Count('motorcycles_ads')).all().values_list('name__username', 'rating',
                                                                                                    'website',
                                                                                                    'description',
                                                                                                    'ads').order_by(
        '-rating')
    return render(request, "dealers.html", {"dealers": dealer})


def dealer(request, name):
    cars = Car.objects.select_related('cars_ads').prefetch_related('cars_ads__dealer').annotate(
        category=Value('cars', output_field=CharField())).filter(cars_ads__dealer__name__username=name).values_list(
        'producer__name', 'model', 'id', 'cars_ads__price', 'cars_ads__date', 'category')
    motorcycles = Motorcycle.objects.select_related('motorcycles_ads').prefetch_related(
        'motorcycles_ads__dealer').annotate(category=Value('motorcycles', output_field=CharField())).filter(
        motorcycles_ads__dealer__name__username=name).values_list('producer__name', 'model', 'id', 'motorcycles_ads__price',
                                                        'motorcycles_ads__date', 'category')
    scooters = Scooter.objects.select_related('scooters_ads').prefetch_related('scooters_ads__dealer').annotate(
        category=Value('scooters', output_field=CharField())).filter(scooters_ads__dealer__name__username=name).values_list(
        'producer__name', 'model', 'id', 'scooters_ads__price', 'scooters_ads__date', 'category')
    product = sorted(chain(cars, motorcycles, scooters), key=lambda instance: instance[4])
    category_name = name + ' ads'
    return render(request, "ads.html", {"products": product, "category_name": category_name})


def registration(request):
    if request.user.is_authenticated:
        return HttpResponseBadRequest("<h1>You are already registered</h1>")
    form = RegistrationUser
    if request.method == 'POST':
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        email = request.POST.get("email")
        is_dealer = request.POST.get("dealer")
        if User.objects.filter(username=username).exists():
            return render(request, "registration/registration.html", {"form": form, "error": "User " + username + " already exists!"})
        if password1 != password2:
            return render(request, "registration/registration.html", {"form": form, "error": "Passwords do not match!"})
        new_user = User(username=username, email=email)
        new_user.set_password(password1)
        new_user.save()
        user = authenticate(username=username, password=password1)
        login(request, user)
        if is_dealer:
            return HttpResponsePermanentRedirect("/dealer_registration/")
        return HttpResponsePermanentRedirect("/")
    else:
        return render(request, "registration/registration.html", {"form": form})


def dealer_registration(request):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("<h1>Bad request</h1>")
    if request.method == 'POST':
        website = request.POST.get("website")
        description = request.POST.get("description")
        Dealer.objects.update_or_create(name=User.objects.get(id=request.user.id), defaults={"website": website, "description": description})
        return HttpResponsePermanentRedirect('/dealers/' + request.user.username)
    else:
        try:
            initial = Dealer.objects.get(name__id=request.user.id)
            initial_dict = {"website": initial.website, "description": initial.description}
        except ObjectDoesNotExist:
            initial_dict = None
        form = RegistrationDealer(initial=initial_dict)
        return render(request, "registration/edit.html", {"form": form})
