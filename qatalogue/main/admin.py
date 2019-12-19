from django.contrib import admin
from .models import Scooter, Motorcycle, Car, Producer, Ad, ScooterAd, MotorcycleAd, CarAd, Dealer, Review


admin.site.register(Scooter)
admin.site.register(Motorcycle)
admin.site.register(Car)
admin.site.register(Producer)
admin.site.register(ScooterAd)
admin.site.register(MotorcycleAd)
admin.site.register(CarAd)
admin.site.register(Dealer)
admin.site.register(Review)
