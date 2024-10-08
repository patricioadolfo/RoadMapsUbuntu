# Generated by Django 5.1 on 2024-08-31 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('route', '0049_alter_route_preparation_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='route',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='route',
            name='preparation_date',
            field=models.DateField(blank=True, default='2024-08-31', null=True, verbose_name='Fecha de Creacion'),
        ),
        migrations.AlterField(
            model_name='route',
            name='preparation_time',
            field=models.TimeField(blank=True, default='01:20:57', null=True, verbose_name='Hora de Creacion'),
        ),
        migrations.AlterField(
            model_name='routeinstance',
            name='instance_date',
            field=models.DateField(blank=True, default='2024-08-31', null=True),
        ),
        migrations.AlterField(
            model_name='routeinstance',
            name='instance_time',
            field=models.TimeField(blank=True, default='01:20:57', null=True, verbose_name='Hora de Creacion'),
        ),
    ]
