from django.db import models

# Create your models here.
class AromaProfile(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return '{}'.format(self.title)
    

class HopManager(models.Manager):
    def all_with_prefetch_beers(self):
        qs = self.get_queryset()
        return qs.prefetch_related('used_hops')

class Hop(models.Model):
    name = models.CharField(max_length=50)

    description = models.TextField(blank=True)
    alpha_min = models.FloatField(null=True, blank=True)
    alpha_max = models.FloatField(null=True, blank=True)

    aroma_profile = models.ManyToManyField(to='AromaProfile', related_name='aroma_profile', blank=True)

    objects = HopManager()

    class Meta:
        ordering = ('name', )
    
    def __str__(self):
        return '{}'.format(self.name)