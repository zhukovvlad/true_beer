# Generated by Django 3.0.4 on 2020-04-19 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0023_auto_20200416_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]