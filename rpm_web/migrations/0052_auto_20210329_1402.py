# Generated by Django 3.2.dev20200924115306 on 2021-03-29 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpm_web', '0051_auto_20210329_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mproject',
            name='date_created',
            field=models.CharField(blank=True, default='29/03/2021-14:02', max_length=50),
        ),
        migrations.AlterField(
            model_name='mrelease_input',
            name='date_created',
            field=models.CharField(blank=True, default='29/03/2021-14:02', max_length=50),
        ),
    ]
