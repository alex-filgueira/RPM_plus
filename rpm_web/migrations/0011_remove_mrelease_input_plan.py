# Generated by Django 3.2.dev20200924115306 on 2021-03-04 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rpm_web', '0010_alter_mrelease_input_plan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mrelease_input',
            name='plan',
        ),
    ]
