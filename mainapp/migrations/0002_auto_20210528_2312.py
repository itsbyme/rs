# Generated by Django 3.0.4 on 2021-05-28 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='create',
            new_name='create_day',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='delete',
            new_name='delete_day',
        ),
    ]