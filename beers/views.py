from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from beers.models import Beer
from .forms import BeerCreateForm

# Create your views here.
def home(request):
    return render(request, 'beers/home.html')

class BeerList(ListView):
    paginate_by = 10
    model = Beer

class BeerDetail(DetailView):
    model = Beer

""" @login_required
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['og'] and request.POST['abv']:
            beer = Beer()
            print(request.POST)
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
        return render(request, 'beers/create.html') """

""" class BeerCreate(LoginRequiredMixin, CreateView):
    def get(self, request):
        form = BeerCreateForm()
        return render(request, 'beers/create.html', context={'form': form})
    def post(self, request):
        print(request.POST)
        bound_form = BeerCreateForm(request.POST)
        print()
        if bound_form.is_valid():
            new_beer = bound_form.save()
            new_beer.hunter = self.request.user
            print(new_beer)
            return redirect(new_beer)
        return render(request, 'beers/create.html', context={'form': bound_form})
    
    #   raise_exception = True """

class BeerCreate(LoginRequiredMixin, CreateView):
    form_class = BeerCreateForm
    template_name = 'beers/create.html'

    def get_initial(self):
        return {
            'hunter': self.request.user.id
        }