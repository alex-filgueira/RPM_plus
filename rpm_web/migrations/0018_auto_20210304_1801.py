# Generated by Django 3.2.dev20200924115306 on 2021-03-04 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpm_web', '0017_auto_20210304_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mproject',
            name='date_end',
            field=models.CharField(blank=True, default='04032021', max_length=50),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_ini',
            field=models.CharField(blank=True, default='04Y032021', max_length=50),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_status',
            field=models.CharField(blank=True, default='04032021', max_length=50),
        ),
        migrations.AlterField(
            model_name='mrelease_input',
            name='date_beantragt',
            field=models.CharField(blank=True, default='04032021', max_length=50),
        ),
    ]
