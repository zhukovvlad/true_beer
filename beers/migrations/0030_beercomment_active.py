# Generated by Django 3.0.4 on 2020-05-01 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0029_auto_20200501_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='beercomment',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
