# Generated by Django 3.0.4 on 2020-04-13 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0014_beer_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beer',
            name='image',
            field=models.ImageField(default='images/default/default_beer.png', null=True, upload_to='images/'),
        ),
    ]