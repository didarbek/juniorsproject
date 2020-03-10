<<<<<<< HEAD
# Generated by Django 2.2.6 on 2020-03-08 14:43
=======
# Generated by Django 2.2.5 on 2020-03-09 15:26
>>>>>>> c08021b3c1c42806fe1f45fa6a62820b61eebd74

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< HEAD
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '__first__'),
=======
        ('groups', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
>>>>>>> c08021b3c1c42806fe1f45fa6a62820b61eebd74
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('slug', models.SlugField(blank=True, max_length=150, null=True)),
                ('body', models.TextField(blank=True, max_length=5000, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='post_photos/')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('rank_score', models.FloatField(default=0.0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_posts', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitted_posts', to='groups.Group')),
                ('mentioned', models.ManyToManyField(blank=True, related_name='m_in_posts', to=settings.AUTH_USER_MODEL)),
                ('points', models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
