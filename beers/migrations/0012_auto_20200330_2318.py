# Generated by Django 3.0.4 on 2020-03-30 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('breweries', '0003_auto_20200324_1625'),
        ('beers', '0011_auto_20200330_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beer',
            name='brewery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewered', to='breweries.Brewery'),
        ),
    ]
