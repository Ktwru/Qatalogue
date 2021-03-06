# Generated by Django 2.2.7 on 2019-11-16 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=50, unique=True)),
                ('year', models.PositiveSmallIntegerField()),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'sedan'), (2, 'hatchback'), (3, 'SUV'), (4, 'station wagon'), (5, 'coupe'), (6, 'minivan')])),
                ('volume', models.PositiveSmallIntegerField()),
                ('power', models.PositiveSmallIntegerField()),
                ('drive', models.PositiveSmallIntegerField(choices=[(1, 'rear'), (2, 'foward'), (3, 'full')])),
                ('pic', models.ImageField(blank=True, default=None, null=True, upload_to='products')),
            ],
        ),
        migrations.CreateModel(
            name='Dealer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('rating', models.SmallIntegerField(default=0)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Motorcycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=50, unique=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'classic'), (2, 'sport bike'), (3, 'street bike'), (4, 'cross bike'), (5, 'cruiser')], default=1)),
                ('cylinders', models.PositiveSmallIntegerField()),
                ('volume', models.PositiveSmallIntegerField()),
                ('power', models.PositiveSmallIntegerField()),
                ('pic', models.ImageField(blank=True, default=None, null=True, upload_to='products')),
            ],
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Scooter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=50, unique=True)),
                ('max_speed', models.PositiveSmallIntegerField()),
                ('power', models.PositiveSmallIntegerField()),
                ('battery_capacity', models.PositiveIntegerField()),
                ('pic', models.ImageField(blank=True, default=None, null=True, upload_to='products')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scooters', to='main.Producer')),
            ],
        ),
        migrations.CreateModel(
            name='ScooterAd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('description', models.TextField(default='')),
                ('date', models.DateTimeField()),
                ('dealer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scooters_ads', to='main.Dealer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scooters_ads', to='main.Scooter', verbose_name='Scooter')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MotorcycleAd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('description', models.TextField(default='')),
                ('date', models.DateTimeField()),
                ('dealer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='motorcycles_ads', to='main.Dealer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='motorcycles_ads', to='main.Motorcycle', verbose_name='Motorcycle')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='motorcycle',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='motorcycles', to='main.Producer'),
        ),
        migrations.CreateModel(
            name='CarAd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('description', models.TextField(default='')),
                ('date', models.DateTimeField()),
                ('dealer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars_ads', to='main.Dealer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars_ads', to='main.Car', verbose_name='Car')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='car',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='main.Producer'),
        ),
    ]
