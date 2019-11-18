from django.shortcuts import render
from django.http import HttpResponseBadRequest
from main.models import *
from django.db.models import Count, Min


def main_paige(request):
    return render(request, "main_page.html")


def ads(request, category):
    if category == 'cars':
        product = Car.objects.select_related('cars_ads').prefetch_related('cars_ads__price').annotate(
            ads=Count('cars_ads'), min=Min('cars_ads__price')).all().values_list('producer__name', 'model', 'ads',
                                                                                 'min', 'id')
        category_name = 'Cars'
    elif category == 'motorcycles':
        product = Motorcycle.objects.select_related('motorcycles_ads').prefetch_related(
            'motorcycles_ads__price').annotate(
            ads=Count('motorcycles_ads'), min=Min('motorcycles_ads__price')).all().values_list('producer__name',
                                                                                               'model', 'ads',
                                                                                               'min', 'id')
        category_name = 'Motorcycles'
    elif category == 'scooters':
        product = Scooter.objects.select_related('scooters_ads').prefetch_related('scooters_ads__price').annotate(
            ads=Count('scooters_ads'), min=Min('scooters_ads__price')).all().values_list('producer__name', 'model',
                                                                                         'ads',
                                                                                         'min', 'id')
        category_name = 'Scooters'
    else:
        return HttpResponseBadRequest("<h1>Bad Request</h1>")
    return render(request, "ads.html", {"products": product, "category_name": category_name})


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
        ads=Count('scooters_ads') + Count('cars_ads') + Count('motorcycles_ads')).all().values_list('name', 'rating',
                                                                                                    'website',
                                                                                                    'description',
                                                                                                    'ads').order_by(
        '-rating')
    return render(request, "dealers.html", {"dealers": dealer})


def dealer(request, name):
    product = CarAd.objects.select_related('cars_ads').prefetch_related('cars_ads__price').annotate(
        ads=Count('cars_ads'), min=Min('cars_ads__price')).filter(dealer=id).values_list('producer__name', 'model', 'ads',
                                                                             'min', 'id', 'dealer')

    cars = CarAd.objects.filter(dealer__name=name).value_list('producer__name', 'model', '', '', 'id')
    motorcycles = MotorcycleAd.objects.filter(dealer__name=name).value_list('producer__name', 'model', '', '', 'id')
    scooters = ScooterAd.objects.filter(dealer__name=name).value_list('producer__name', 'model', '', '', 'id')
    category_name = name + 'ads'
    return render(request, "ads.html", {"products": product, "category_name": category_name})
