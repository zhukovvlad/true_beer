# Generated by Django 3.0.4 on 2020-03-20 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breweries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BreweryManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
