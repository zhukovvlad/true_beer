from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required

from beers.models import Beer

# Create your views here.
def home(request):
    return render(request, 'beers/home.html')

class BeerList(ListView):
    model = Beer

class BeerDetail(DetailView):
    model = Beer

@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['og'] and request.POST['abv']:
            beer = Beer()
            beer.title = request.POST['title']
            beer.description = request.POST['description']
            beer.og = request.POST['og']
            beer.abv = request.POST['abv']
            beer.ibu = request.POST['ibu']
            beer.icon = request.FILES['icon']
            beer.image = request.FILES['image']
            beer.hunter = request.user
            beer.save()
            return redirect('beer:BeerList')
        else:
            return render(request, 'beers/create.html', {'error': 'All fields with * are required'})
    else:
        return render(request, 'beers/create.html')