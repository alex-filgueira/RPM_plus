# Generated by Django 3.2.dev20200924115306 on 2021-03-24 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpm_web', '0038_auto_20210322_0836'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MPlan',
        ),
        migrations.DeleteModel(
            name='MType_input',
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_end',
            field=models.CharField(blank=True, default='2021-03-24', max_length=50),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_ini',
            field=models.CharField(blank=True, default='2021-03-24', max_length=50),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_status',
            field=models.CharField(blank=True, default='2021-03-24', max_length=50),
        ),
        migrations.AlterField(
            model_name='mrelease_input',
            name='date_beantragt',
            field=models.CharField(blank=True, default='24032021', max_length=50),
        ),
    ]