# Generated by Django 3.0.4 on 2020-04-11 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
        ('breweries', '0006_auto_20200411_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='brewery',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='addresses.Country'),
        ),
    ]
