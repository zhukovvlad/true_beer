from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Brewery

# Create your views here.

class BreweryList(ListView):
    model = Brewery

class BreweryDetail(DetailView):
    model = Brewery