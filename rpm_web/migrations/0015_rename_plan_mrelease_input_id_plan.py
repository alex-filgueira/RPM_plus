# Generated by Django 3.2.dev20200924115306 on 2021-03-04 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rpm_web', '0014_auto_20210304_1246'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mrelease_input',
            old_name='plan',
            new_name='id_plan',
        ),
    ]
