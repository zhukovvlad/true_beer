from django.db import models
from django.shortcuts import reverse
from django.core.exceptions import ValidationError
import django.contrib.auth
from django.contrib.auth.models import User
from breweries.models import Brewery
from hops.models import Hop

from .validators import validate_title

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Sum
from django.utils.text import slugify


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug

# Create your models here.
class BeerManager(models.Manager):

    def all_with_related_instances(self):
        qs = self.get_queryset()
        qs = qs.select_related(
            'brewery', 'style'
        )
        qs = qs.prefetch_related(
            'hops'
        )
        return qs

    def all_with_related_instances_and_score(self):
        qs = self.all_with_related_instances()
        qs = qs.annotate(score=Sum('vote__value'))
        return qs

    def top_beers(self, limit=10):
        qs = self.get_queryset()
        qs = qs.annotate(vote_sum=Sum('vote__value'))
        qs = qs.exclude(vote_sum=None)
        qs = qs.order_by('-vote_sum')
        qs = qs[:limit]
        return qs


class Beer(models.Model):
    title = models.CharField(max_length=140, db_index=True, validators=[validate_title])
    version = models.CharField(max_length=140, null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)

    og = models.FloatField(null=True, blank=True)
    abv = models.FloatField(null=True, blank=True)
    ibu = models.FloatField(null=True, blank=True)

    image = models.ImageField(upload_to='images/', default='images/default/default_beer.png', null=True, blank=True)
    icon = models.ImageField(upload_to='images/', default='images/default/default_beer.png', null=True)

    votes_total = models.IntegerField(default=1)

    hunter = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    hops = models.ManyToManyField(Hop, related_name='used_hops', blank=True)

    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE, related_name='brewered', null=True)
    style = models.ForeignKey(to='Style', on_delete=models.SET_NULL, null=True, blank=True)

    date_pub = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True)

    objects = BeerManager()
    
    def get_absolute_url(self):
        return reverse("beer:BeerDetail", kwargs={"slug": self.slug})
    
    def title_for_render(self):
        title_list = self.title.split(' ')
        title_list = (x.capitalize() for x in title_list)
        title_list = list(title_list)
        title_list = ' '.join(str(x) for x in title_list)
        return title_list
    
    class Meta:
        ordering = ('title', )
        constraints = [
            models.UniqueConstraint(fields=['title', 'version', 'brewery'], name='beer_constraint')
        ]

    def __str__(self):
        return '{}'.format(self.title)
    
    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        if not self.id:
            if self.version:
                new_slug = self.title + ' ' + self.version + ' by ' + str(self.brewery.name)
            else:
                new_slug = self.title + ' by ' + self.brewery.name
            self.slug = gen_slug(new_slug)
        super().save(*args, **kwargs)


class Style(models.Model):
    short_title = models.CharField(max_length=40, null=True, blank=True)
    title = models.CharField(max_length=140)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.short_title)


class VoteManager(models.Manager):
    def get_vote_or_unsaved_blank_vote(self, beer, user):
        try:
            return Vote.objects.get(
                beer=beer,
                user=user)
        except ObjectDoesNotExist:
            return Vote(
                beer=beer,
                user=user)


class Vote(models.Model):
    UP = 1
    DOWN = -1
    VALUE_CHOICES = (
        (UP, "UpVote"),
        (DOWN, "DownVote")
    )
    value = models.SmallIntegerField(
        choices=VALUE_CHOICES,
    )

    user = models.ForeignKey(
        django.contrib.auth.get_user_model(),
        on_delete=models.CASCADE
        )

    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)

    voted_on = models.DateTimeField(auto_now=True)

    objects = VoteManager()

    class Meta:
        unique_together = ('user', 'beer', )
