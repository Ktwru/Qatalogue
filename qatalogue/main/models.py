from django.db import models


class Scooter(models.Model):
    model = models.CharField(blank=False, null=False, unique=True)
    producer = models.ForeignKey('Producer', models.CASCADE, 'scooters')
    maxSpeed = models.PositiveSmallIntegerField(blank=False, null=False)
    power = models.PositiveSmallIntegerField(blank=False, null=False)
    batteryCapacity = models.PositiveIntegerField(blank=False, null=False)
    pic = models.ImageField(null=True, blank=True, upload_to='products', default=None)

    def __str__(self):
        return self.producer.name + self.model


class Motorcycle(models.Model):
    MOTORCYCLE_TYPE_CHOICES = {'classic': 1, 'sport bike': 2, 'street bike': 3, 'cross bike': 4, 'cruiser': 5}
    model = models.CharField(blank=False, null=False, unique=True)
    producer = models.ForeignKey('Producer', models.CASCADE, 'motorcycles')
    type = models.PositiveSmallIntegerField(blank=False, null=False, default=1, choices=MOTORCYCLE_TYPE_CHOICES)
    cylinders = models.PositiveSmallIntegerField(blank=False, null=False)
    volume = models.PositiveSmallIntegerField(blank=False, null=False)
    power = models.PositiveSmallIntegerField(blank=False, null=False)
    pic = models.ImageField(null=True, blank=True, upload_to='products', default=None)

    def __str__(self):
        return self.producer.name + self.model


class Car(models.Model):
    CAR_TYPE_CHOICES = {'sedan': 1, 'hatchback': 2, 'SUV': 3, 'station wagon': 4, 'coupe': 5, 'minivan': 6}
    CAR_DRIVE_CHOICES = {'rear': 1, 'foward': 2, 'full': 3}
    model = models.CharField(blank=False, null=False, unique=True)
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
    name = models.CharField(blank=False, null=False, unique=True)
    country = models.CharField(blank=True, null=True)
    website = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.name


class Ad(models.Model):
    class Meta:
        abstract = True
    price = models.PositiveIntegerField(blank=False, null=False)
    description = models.TextField(default='')
    dealer = models.ManyToManyField('Dealer', 'ads', on_delete=models.CASCADE)
    date = models.DateTimeField(blank=False, null=False)


class ScooterAd(Ad):
    product = models.ManyToManyField('Scooter', 'ads', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + self.dealer


class MotorcycleAd(Ad):
    product = models.ManyToManyField('Motorcycle', 'ads', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + self.dealer


class CarAd(Ad):
    product = models.ManyToManyField('Car', 'ads', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + self.dealer


class Dealer(models.Model):
    name = models.CharField(blank=False, null=False, unique=True)
    rating = models.SmallIntegerField(default=0)
    website = models.CharField(blank=True, null=True)
    description = models.TextField(default='')

    def __str__(self):
        return self.name


