# Generated by Django 3.0.4 on 2020-05-21 18:08

import breweries.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breweries', '0009_brewery_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='brewery',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='brewery',
            name='image',
            field=models.ImageField(blank=True, default='images/default/fermentation.png', null=True, upload_to=breweries.models.brewery_directory_path_with_uuid),
        ),
    ]