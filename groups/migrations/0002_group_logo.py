# Generated by Django 2.2.6 on 2020-03-08 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='logo',
            field=models.ImageField(blank=True, upload_to='group_logos/'),
        ),
    ]