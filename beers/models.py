from django.db import models
from django.contrib.auth.models import User
from breweries.models import Brewery

# Create your models here.
class Beer(models.Model):
    title = models.CharField(max_length=140)
    description = models.TextField(null=True, blank=True)

    og = models.FloatField(null=True, blank=True)
    abv = models.FloatField(null=True, blank=True)
    ibu = models.FloatField(null=True, blank=True)

    image = models.ImageField(upload_to='images/', null=True)
    icon = models.ImageField(upload_to='images/', default='images/default/default_beer.png')

    votes_total = models.IntegerField(default=1)

    hunter = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    hops = models.ManyToManyField(to='Hop', related_name='used_hops', blank=True)

    brewery = models.ForeignKey(Brewery, on_delete=models.SET_NULL, related_name='brewered', null=True, blank=True)
    style = models.ForeignKey(to='Style', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return '{}'.format(self.title)


class Style(models.Model):
    short_title = models.CharField(max_length=40, null=True, blank=True)
    title = models.CharField(max_length=140)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.short_title)


class Hop(models.Model):
    name = models.CharField(max_length=50)

    description = models.TextField(blank=True)
    alpha_min = models.FloatField(null=True, blank=True)
    alpha_max = models.FloatField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)
