# Generated by Django 2.2.7 on 2019-11-16 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carad',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars_ads', to='main.Car'),
        ),
        migrations.AlterField(
            model_name='motorcyclead',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='motorcycles_ads', to='main.Motorcycle'),
        ),
        migrations.AlterField(
            model_name='scooterad',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scooters_ads', to='main.Scooter'),
        ),
    ]
