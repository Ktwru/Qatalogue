from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponsePermanentRedirect
from main.models import *
from django.db.models import Count, Min, Value, CharField, Q
from itertools import chain
from .forms import RegistrationUser, RegistrationDealer
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from .filters import CarFilter, MotorcycleFilter, ScooterFilter
from django.forms.models import modelform_factory, modelformset_factory, formset_factory


def main_paige(request):
    return render(request, "main_page.html")


def ads(request, category):
    if category == 'cars':
        product = Car.objects.select_related().prefetch_related().annotate(
            ads=Count('cars_ads'), min=Min('cars_ads__price')).all()
        category_name = 'Cars'
        product_filter = CarFilter(request.GET, queryset=product)
    elif category == 'motorcycles':  # ------------------------------------------
        product = Motorcycle.objects.select_related().prefetch_related(
        ).annotate(
            ads=Count('motorcycles_ads'), min=Min('motorcycles_ads__price')).all()
        category_name = 'Motorcycles'
        product_filter = MotorcycleFilter(request.GET, queryset=product)
    elif category == 'scooters':
        product = Scooter.objects.select_related().prefetch_related().annotate(
            ads=Count('scooters_ads'), min=Min('scooters_ads__price')).all()
        category_name = 'Scooters'
        product_filter = ScooterFilter(request.GET, queryset=product)
    else:
        return HttpResponseBadRequest("<h1>Bad Request</h1>")
    return render(request, "ads.html", {"products": product, "category_name": category_name,
                                        "category": category, "filter": product_filter})


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
        ads=Count('scooters_ads') + Count('cars_ads') + Count('motorcycles_ads')).all().values_list('name__username',
                                                                                                    'rating',
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
        motorcycles_ads__dealer__name__username=name).values_list('producer__name', 'model', 'id',
                                                                  'motorcycles_ads__price',
                                                                  'motorcycles_ads__date', 'category')
    scooters = Scooter.objects.select_related('scooters_ads').prefetch_related('scooters_ads__dealer').annotate(
        category=Value('scooters', output_field=CharField())).filter(
        scooters_ads__dealer__name__username=name).values_list(
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
            return render(request, "registration/registration.html",
                          {"form": form, "error": "User " + username + " already exists!"})
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
        Dealer.objects.update_or_create(name=User.objects.get(id=request.user.id),
                                        defaults={"website": website, "description": description})
        return HttpResponsePermanentRedirect('/dealers/' + request.user.username)
    else:
        try:
            initial = Dealer.objects.get(name__id=request.user.id)
            initial_dict = {"website": initial.website, "description": initial.description}
        except ObjectDoesNotExist:
            initial_dict = None
        form = RegistrationDealer(initial=initial_dict)
        return render(request, "registration/edit.html", {"form": form})


def search(request):
    mark = request.GET.get('mark')
    cars = Car.objects.select_related('cars_ads', 'producer').prefetch_related('producer__name').annotate(
        category=Value('cars', output_field=CharField()),
        ads=Count('cars_ads'), min=Min('cars_ads__price')).filter(
        Q(producer__name__icontains=mark) | Q(model__icontains=mark)).values_list(
        'producer__name', 'model', 'category', 'id', 'ads', 'min')
    motorcycles = Motorcycle.objects.select_related('motorcycles_ads', 'producer').prefetch_related(
        'producer__name').annotate(
        category=Value('motorcycles', output_field=CharField()),
        ads=Count('motorcycles_ads'), min=Min('motorcycles_ads__price')).filter(
        Q(producer__name__icontains=mark) | Q(model__icontains=mark)).values_list(
        'producer__name', 'model', 'category', 'id', 'ads', 'min')
    scooters = Scooter.objects.select_related('scooters_ads', 'producer').prefetch_related('producer__name').annotate(
        category=Value('scooters', output_field=CharField()),
        ads=Count('scooters_ads'), min=Min('scooters_ads__price')).filter(
        Q(producer__name__icontains=mark) | Q(model__icontains=mark)).values_list(
        'producer__name', 'model', 'category', 'id', 'ads', 'min')

    product = sorted(chain(cars, motorcycles, scooters), key=lambda instance: instance[3])
    return render(request, "search.html", {"products": product})


def add_ad(request, category):
    if not Dealer.objects.filter(name=request.user.id, valid=True).exists():
        return HttpResponseBadRequest("<h1>You are not an validated dealer!</h1>")
    if category == 'cars':
        model = CarAd
    elif category == 'motorcycles':
        model = MotorcycleAd
    elif category == 'scooters':
        model = ScooterAd
    else:
        return HttpResponseBadRequest("<h1>Bad Request</h1>")
    form = modelform_factory(model, fields=('product', 'description', 'price'),
                             help_texts={'product': '<a href=\"/ads/' + category + "/add_product\">Add</a>"})
    if request.method == 'POST':
        new_ad = form(request.POST).save(commit=False)
        new_ad.dealer = Dealer.objects.get(name=request.user.id)
        new_ad.save()
        return HttpResponsePermanentRedirect('/ads/' + category)
    else:
        if request.GET.get('id'):
            form = form(initial={'product': request.GET.get('id')})
        return render(request, "new_ad.html", {"form": form})


def add_product(request, category):
    if not Dealer.objects.filter(name=request.user.id, valid=True).exists():
        return HttpResponseBadRequest("<h1>You are not an validated dealer!</h1>")
    if category == 'cars':
        model = Car
        form_fields = ('producer', 'model', 'type', 'year', 'volume', 'power', 'drive', 'pic')
        form_labels = {'drive': "Drive unit"}
    elif category == 'motorcycles':
        model = Motorcycle
        form_fields = ('producer', 'model', 'type', 'cylinders', 'volume', 'power', 'pic')
        form_labels = {'cylinders': "Number of cylinders"}
    elif category == 'scooters':
        model = Scooter
        form_fields = ('producer', 'model', 'max_speed', 'battery_capacity', 'power', 'pic')
        form_labels = {'max_speed': "Max speed", 'battery_capacity': "Battery capacity"}
    else:
        return HttpResponseBadRequest("<h1>Bad Request</h1>")
    form = modelform_factory(model, fields=form_fields, labels=form_labels)
    if request.method == 'POST':
        form(request.POST, request.FILES).save()
        return HttpResponsePermanentRedirect('/ads/' + category)
    else:
        return render(request, "new_ad.html", {"form": form})
