# Generated by Django 3.0.4 on 2020-05-20 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0034_auto_20200519_1750'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='style',
            options={'ordering': ('short_title',)},
        ),
    ]