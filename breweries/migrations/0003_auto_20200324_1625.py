# Generated by Django 3.0.4 on 2020-03-24 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('breweries', '0002_brewerymanager'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brewery',
            options={'ordering': ('name',), 'verbose_name_plural': 'Breweries'},
        ),
    ]
