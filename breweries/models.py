from django.db import models

# Create your models here.
class BreweryManager(models.Model):
    def all_with_prefetch_beers(self):
        qs = self.get_queryset()
        return qs.prefetch_related('brewered')

class Brewery(models.Model):
    name = models.CharField(max_length=140, verbose_name='Brewery\'s name')

    objects = BreweryManager()

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Breweries'

    def __str__(self):
        return '{}'.format(self.name)
