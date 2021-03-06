# Generated by Django 3.2.dev20200924115306 on 2021-03-25 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpm_web', '0041_alter_mrelease_input_id_ecu'),
    ]

    operations = [
        migrations.AddField(
            model_name='mproject',
            name='date_created',
            field=models.CharField(blank=True, default='2021-03-25', max_length=50),
        ),
        migrations.AddField(
            model_name='mrelease_input',
            name='date_created',
            field=models.CharField(blank=True, default='25032021', max_length=50),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_end',
            field=models.CharField(blank=True, default='2021-03-25', max_length=50),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_ini',
            field=models.CharField(blank=True, default='2021-03-25', max_length=50),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_status',
            field=models.CharField(blank=True, default='2021-03-25', max_length=50),
        ),
        migrations.AlterField(
            model_name='mrelease_input',
            name='date_beantragt',
            field=models.CharField(blank=True, default='25032021', max_length=50),
        ),
    ]
