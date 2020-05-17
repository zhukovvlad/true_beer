from django.db import models
from django.utils.text import slugify
from django.db.models.aggregates import Sum

from addresses.models import Country

def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    if "brewery" in new_slug:
        return new_slug
    return new_slug + '-brewery'

# Create your models here.
class BreweryManager(models.Manager):
    def all_with_prefetch_beers(self):
        qs = self.get_queryset()
        return qs.prefetch_related('brewered')
    
    def all_with_prefetch_beers_and_score(self):
        qs = self.all_with_prefetch_beers()
        qs = qs.annotate(total_rating=Sum('vote__value'))
        return qs

class Brewery(models.Model):
    name = models.CharField(max_length=140, verbose_name='Brewery\'s name')
    slug = models.SlugField(blank=True)

    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)

    objects = BreweryManager()

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Breweries'

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)
