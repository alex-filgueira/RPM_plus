# Generated by Django 3.2.dev20200924115306 on 2021-04-15 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpm_web', '0056_auto_20210413_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mproject',
            name='date_created',
            field=models.CharField(blank=True, default='15/04/2021-12:44', max_length=50),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_end',
            field=models.CharField(blank=True, default='2021-04-15', max_length=50),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_ini',
            field=models.CharField(blank=True, default='2021-04-15', max_length=50),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_status',
            field=models.CharField(blank=True, default='2021-04-15', max_length=50),
        ),
        migrations.AlterField(
            model_name='mrelease_input',
            name='date_beantragt',
            field=models.CharField(blank=True, default='15042021', max_length=50),
        ),
        migrations.AlterField(
            model_name='mrelease_input',
            name='date_created',
            field=models.CharField(blank=True, default='15/04/2021-12:44', max_length=50),
        ),
    ]
