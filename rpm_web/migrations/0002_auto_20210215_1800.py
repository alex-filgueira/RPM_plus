# Generated by Django 3.2.dev20200924115306 on 2021-02-15 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rpm_web', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mrelease_input',
            old_name='date',
            new_name='date_beantragt',
        ),
        migrations.RenameField(
            model_name='mrelease_input',
            old_name='name',
            new_name='n_version',
        ),
    ]
