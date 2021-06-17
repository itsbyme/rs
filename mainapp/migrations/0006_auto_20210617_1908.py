# Generated by Django 3.0.4 on 2021-06-17 16:08

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20210617_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='RU', unique=True, verbose_name='Телефон'),
        ),
    ]
