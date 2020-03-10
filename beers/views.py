from django.shortcuts import render
from django.views.generic import ListView, DetailView

from beers.models import Beer

# Create your views here.
def home(request):
    return render(request, 'beers/home.html')

class BeerList(ListView):
    model = Beer

class BeerDetail(DetailView):
    model = Beer
