from django.db import models
from django.contrib.auth.models import User


class Scooter(models.Model):
    model = models.CharField(blank=False, null=False, unique=True, max_length=50)
    producer = models.ForeignKey('Producer', models.CASCADE, 'scooters')
    max_speed = models.PositiveSmallIntegerField(blank=False, null=False)
    power = models.PositiveSmallIntegerField(blank=False, null=False)
    battery_capacity = models.PositiveIntegerField(blank=False, null=False)
    pic = models.ImageField(null=True, blank=True, upload_to='products', default=None)

    def __str__(self):
        return self.producer.name + self.model


class Motorcycle(models.Model):
    MOTORCYCLE_TYPE_CHOICES = ((1, 'classic'), (2, 'sport bike'), (3, 'street bike'), (4, 'cross bike'), (5, 'cruiser'))
    model = models.CharField(blank=False, null=False, unique=True, max_length=50)
    producer = models.ForeignKey('Producer', models.CASCADE, 'motorcycles')
    type = models.PositiveSmallIntegerField(blank=False, null=False, default=1, choices=MOTORCYCLE_TYPE_CHOICES)
    cylinders = models.PositiveSmallIntegerField(blank=False, null=False)
    volume = models.PositiveSmallIntegerField(blank=False, null=False)
    power = models.PositiveSmallIntegerField(blank=False, null=False)
    pic = models.ImageField(null=True, blank=True, upload_to='products', default=None)

    def __str__(self):
        return self.producer.name + self.model


class Car(models.Model):
    CAR_TYPE_CHOICES = ((1, 'sedan'), (2, 'hatchback'), (3, 'SUV'), (4, 'station wagon'), (5, 'coupe'), (6, 'minivan'))
    CAR_DRIVE_CHOICES = ((1, 'rear'), ( 2, 'foward'), (3, 'full'))
    model = models.CharField(blank=False, null=False, unique=True, max_length=50)
    producer = models.ForeignKey('Producer', models.CASCADE, 'cars')
    year = models.PositiveSmallIntegerField(blank=False, null=False)
    type = models.PositiveSmallIntegerField(blank=False, null=False, choices=CAR_TYPE_CHOICES)
    volume = models.PositiveSmallIntegerField(blank=False, null=False)
    power = models.PositiveSmallIntegerField(blank=False, null=False)
    drive = models.PositiveSmallIntegerField(blank=False, null=False, choices=CAR_DRIVE_CHOICES)
    pic = models.ImageField(null=True, blank=True, upload_to='products', default=None)

    def __str__(self):
        return self.producer.name + self.model


class Producer(models.Model):
    name = models.CharField(blank=False, null=False, unique=True, max_length=50)
    country = models.CharField(blank=True, null=True, max_length=100)
    website = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return self.name


class Ad(models.Model):
    class Meta:
        abstract = True
    price = models.PositiveIntegerField(blank=False, null=False)
    description = models.TextField(default='')
    date = models.DateTimeField(blank=False, null=False)


class ScooterAd(Ad):
    dealer = models.ForeignKey('Dealer', models.CASCADE, 'scooters_ads')
    product = models.ForeignKey('Scooter', models.CASCADE, 'scooters_ads')

    def __str__(self):
        return self.product.name + self.dealer


class MotorcycleAd(Ad):
    dealer = models.ForeignKey('Dealer', models.CASCADE, 'motorcycles_ads')
    product = models.ForeignKey('Motorcycle', models.CASCADE, 'motorcycles_ads')

    def __str__(self):
        return self.product.name + self.dealer


class CarAd(Ad):
    dealer = models.ForeignKey('Dealer', models.CASCADE, 'cars_ads')
    product = models.ForeignKey('Car', models.CASCADE, 'cars_ads')

    def __str__(self):
        return self.product.model + ' ' + self.product.producer.name + ' ' + self.dealer.name


class Dealer(models.Model):
    name = models.OneToOneField(User, models.CASCADE)
    rating = models.SmallIntegerField(default=0)
    website = models.CharField(blank=True, null=True, max_length=100)
    description = models.TextField(default='')
    valid = models.BooleanField(default=False)

    def __str__(self):
        val = " [unvalidated]"
        if self.valid:
            val = ""
        return self.name.username + val


