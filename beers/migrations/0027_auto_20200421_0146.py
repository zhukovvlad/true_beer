# Generated by Django 3.0.4 on 2020-04-20 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0026_auto_20200421_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beer',
            name='slug',
            field=models.SlugField(auto_created=True, blank=True, editable=False),
        ),
    ]
