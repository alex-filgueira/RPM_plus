# Generated by Django 3.2.dev20200924115306 on 2021-03-04 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpm_web', '0015_rename_plan_mrelease_input_id_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mrelease_input',
            name='date_beantragt',
            field=models.CharField(blank=True, default='20210304', max_length=50),
        ),
    ]
