from django.db import models
from django.contrib.auth.models import User
from breweries.models import Brewery
from hops.models import Hop

# Create your models here.
class Beer(models.Model):
    title = models.CharField(max_length=140)
    description = models.TextField(null=True, blank=True)

    og = models.FloatField(null=True, blank=True)
    abv = models.FloatField(null=True, blank=True)
    ibu = models.FloatField(null=True, blank=True)

    image = models.ImageField(upload_to='images/', null=True, blank=True)
    icon = models.ImageField(upload_to='images/', default='images/default/default_beer.png', null=True)

    votes_total = models.IntegerField(default=1)

    hunter = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    hops = models.ManyToManyField(Hop, related_name='used_hops', blank=True)

    brewery = models.ForeignKey(Brewery, on_delete=models.SET_NULL, related_name='brewered', null=True, blank=True)
    style = models.ForeignKey(to='Style', on_delete=models.SET_NULL, null=True, blank=True)

    def amount_hops(self):
        return len(self.hops.all())
    
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
