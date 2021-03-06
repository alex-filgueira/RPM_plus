# Generated by Django 3.2.dev20200924115306 on 2021-03-29 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpm_web', '0050_auto_20210326_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='mecu',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_created',
            field=models.CharField(blank=True, default='29/03/2021-10:31', max_length=50),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_end',
            field=models.CharField(blank=True, default='2021-03-29', max_length=50),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_ini',
            field=models.CharField(blank=True, default='2021-03-29', max_length=50),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_status',
            field=models.CharField(blank=True, default='2021-03-29', max_length=50),
        ),
        migrations.AlterField(
            model_name='mrelease_input',
            name='date_beantragt',
            field=models.CharField(blank=True, default='29032021', max_length=50),
        ),
        migrations.AlterField(
            model_name='mrelease_input',
            name='date_created',
            field=models.CharField(blank=True, default='29/03/2021-10:31', max_length=50),
        ),
    ]
