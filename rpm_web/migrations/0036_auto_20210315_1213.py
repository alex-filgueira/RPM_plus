# Generated by Django 3.2.dev20200924115306 on 2021-03-15 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rpm_web', '0035_auto_20210315_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mrelease_input',
            name='id_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rpm_web.mplan2'),
        ),
        migrations.AlterField(
            model_name='mrelease_input',
            name='id_type_input',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rpm_web.mtype_input2'),
        ),
    ]
