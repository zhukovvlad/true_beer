import os
from uuid import uuid4
from django.db import models
from django.utils.text import slugify
from django.db.models.aggregates import Sum
from django.utils.timezone import now as timezone_now
from django.shortcuts import reverse

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from addresses.models import Country

def brewery_directory_path_with_uuid(instance, filename):
    now = timezone_now()
    base, extension = os.path.splitext(filename)
    extension = extension.lower()
    uuid_for_url = uuid4()
    return f"{now:%Y/%m}/breweries/{uuid_for_url}{instance.pk}{extension}"

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

    description = models.TextField(null=True, blank=True)

    image = models.ImageField(upload_to=brewery_directory_path_with_uuid, default='images/default/fermentation.png', null=True, blank=True)
    icon = ImageSpecField(
        source='image',
        processors=[ResizeToFill(100, 100)],
        format='PNG',
        options={'quality': 60}
    )

    is_verified = models.BooleanField(default=False)

    objects = BreweryManager()

    def get_absolute_url(self):
        return reverse("brewery:BreweryDetail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Breweries'

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)
