# Generated by Django 4.2.17 on 2024-12-18 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0005_post_image_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/'),
        ),
    ]
