# Generated by Django 3.0.4 on 2020-04-13 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0015_auto_20200413_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beer',
            name='image',
            field=models.ImageField(blank=True, default='images/default/default_beer.png', null=True, upload_to='images/'),
        ),
    ]
