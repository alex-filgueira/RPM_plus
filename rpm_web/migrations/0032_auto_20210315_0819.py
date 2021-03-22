# Generated by Django 3.2.dev20200924115306 on 2021-03-15 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpm_web', '0031_mplan2_mtype_input2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mconfig_prj',
            name='fig1_border_w',
        ),
        migrations.RemoveField(
            model_name='mconfig_prj',
            name='fig1_color_1',
        ),
        migrations.RemoveField(
            model_name='mconfig_prj',
            name='fig1_color_2',
        ),
        migrations.RemoveField(
            model_name='mconfig_prj',
            name='fig1_color_3',
        ),
        migrations.RemoveField(
            model_name='mconfig_prj',
            name='fig1_name',
        ),
        migrations.RemoveField(
            model_name='mconfig_prj',
            name='fig1_s',
        ),
        migrations.AddField(
            model_name='mplan2',
            name='fig1_border_w',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='mplan2',
            name='fig1_color_1',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='mplan2',
            name='fig1_color_2',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='mplan2',
            name='fig1_color_3',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='mtype_input2',
            name='fig1_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='mtype_input2',
            name='fig1_s',
            field=models.FloatField(default=0.28),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_end',
            field=models.CharField(blank=True, default='15032021', max_length=50),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_ini',
            field=models.CharField(blank=True, default='15Y032021', max_length=50),
        ),
        migrations.AlterField(
            model_name='mproject',
            name='date_status',
            field=models.CharField(blank=True, default='15032021', max_length=50),
        ),
        migrations.AlterField(
            model_name='mrelease_input',
            name='date_beantragt',
            field=models.CharField(blank=True, default='15032021', max_length=50),
        ),
    ]
