# Generated by Django 3.0.4 on 2020-04-11 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0013_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer',
            name='version',
            field=models.CharField(blank=True, db_index=True, max_length=140, null=True),
        ),
    ]