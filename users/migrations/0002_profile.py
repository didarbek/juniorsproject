# Generated by Django 2.2.5 on 2020-02-26 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_profile', models.ImageField(upload_to=users.models.user_directory_path, verbose_name='image profile')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Birth date')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('countries', django_countries.fields.CountryField(max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
