from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Brewery
from beers.models import Beer

# Create your views here.

class BreweryList(ListView):
    model = Brewery

    context_object_name = "brewery_list"

class BreweryDetail(DetailView):
    # model = Brewery
    queryset = Brewery.objects.all_with_prefetch_beers()

    def get_context_data(self, **kwargs):
        print(self)
        ctx = super().get_context_data(**kwargs)
        print('initial Brewery ctx is, ', ctx)
        qs_beers = Beer.objects.all_with_related_instances_and_score()
        print('qs_beers are, ', qs_beers)
        brewery_beers = qs_beers.filter(brewery=ctx['brewery'])
        brewery_rating = 0
        for item in brewery_beers:
            if not item.score:
                item.score = 0
            brewery_rating += item.score
        brewery_rating = brewery_rating / len(brewery_beers)

        ctx['connected_beers'] = brewery_beers
        ctx['rating'] = brewery_rating
        print('Final Brewery ctx is, ', ctx)
        return ctx