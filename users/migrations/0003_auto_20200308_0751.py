# Generated by Django 2.2.6 on 2020-03-08 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='countries',
            new_name='country',
        ),
    ]
