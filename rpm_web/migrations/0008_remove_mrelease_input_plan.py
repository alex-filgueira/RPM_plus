# Generated by Django 3.2.dev20200924115306 on 2021-03-04 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rpm_web', '0007_auto_20210304_1237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mrelease_input',
            name='plan',
        ),
    ]
