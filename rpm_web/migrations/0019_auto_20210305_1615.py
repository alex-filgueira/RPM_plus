# Generated by Django 3.2.dev20200924115306 on 2021-03-05 15:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpm_web', '0018_auto_20210304_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mproject',
            name='date_end',
            field=models.CharField(blank=True, default='05032021', max_length=50),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_ini',
            field=models.CharField(blank=True, default='05Y032021', max_length=50),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_status',
            field=models.CharField(blank=True, default='05032021', max_length=50),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='factor_weeks',
            field=models.IntegerField(blank=True, default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='max_ecu_slide',
            field=models.IntegerField(blank=True, default=8, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='mrelease_input',
            name='date_beantragt',
            field=models.CharField(blank=True, default='05032021', max_length=50),
        ),
    ]
