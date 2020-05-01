# Generated by Django 3.0.4 on 2020-05-01 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0027_auto_20200421_0146'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('beer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='beers.Beer')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
