# Generated by Django 3.2.dev20200924115306 on 2021-04-13 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpm_web', '0055_auto_20210413_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mproject',
            name='date_created',
            field=models.CharField(blank=True, default='13/04/2021-10:07', max_length=50),
        ),
        migrations.AlterField(
            model_name='mrelease_input',
            name='date_created',
            field=models.CharField(blank=True, default='13/04/2021-10:07', max_length=50),
        ),
    ]
