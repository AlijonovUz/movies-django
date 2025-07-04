# Generated by Django 5.1.6 on 2025-07-02 17:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='duration',
            field=models.CharField(default='1 soat 40 daqiqa', max_length=20, verbose_name='Davomiyligi'),
        ),
        migrations.AlterField(
            model_name='movies',
            name='language',
            field=models.CharField(choices=[("O'zbek tilida", "O'zbek tilida"), ('Rus tilida', 'Rus tilida'), ('Ingliz tilida', 'Ingliz tilida')], max_length=13, verbose_name='Tili'),
        ),
        migrations.AlterField(
            model_name='movies',
            name='year',
            field=models.IntegerField(default=1900, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2025)], verbose_name='Yili'),
        ),
    ]
