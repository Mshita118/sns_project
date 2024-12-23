# Generated by Django 4.2.17 on 2024-12-24 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timeline', '0007_alter_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_image/')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='cover_images/')),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='timeline_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
