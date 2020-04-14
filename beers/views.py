from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from beers.models import Beer, Vote
from .forms import BeerCreateForm, VoteForm

# Create your views here.
def home(request):
    return render(request, 'beers/home.html')

class BeerList(ListView):
    paginate_by = 10
    # model = Beer
    queryset = Beer.objects.all_with_related_instances_and_score()

    context_object_name = 'beer_list'

class BeerDetail(DetailView):
    queryset = Beer.objects.all_with_related_instances_and_score()
    print('Queryset is ', queryset)
    
    def get_context_data(self, **kwargs):
        print('object is ', self.object)
        print('request is ', self.request)
        print('user is ', self.request.user)
        ctx = super().get_context_data(**kwargs)
        print('initial ctx ', ctx)
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                beer=self.object,
                user=self.request.user
            )

            if vote.id:
                vote_form_url = reverse(
                    'beer:UpdateVote',
                    kwargs = {
                        'beer_id': vote.beer.id,
                        'pk': vote.id
                    }
                )
            else:
                vote_form_url = (
                    reverse(
                    'beer:CreateVote',
                    kwargs={
                        'beer_id': self.object.id
                    })
                )
            vote_form = VoteForm(instance=vote)
            ctx['vote_form'] = vote_form
            ctx['vote_form_url'] = vote_form_url
        print('final context is ', ctx)
        return ctx


class CreateVote(LoginRequiredMixin, CreateView):
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        print('start initial is ', initial)
        initial['user'] = self.request.user.id
        initial['beer'] = self.kwargs['beer_id']
        print('final initial is ', initial)
        return initial
    
    def get_success_url(self):
        beer_id = self.object.beer.id
        return reverse(
            'beer:BeerDetail',
            kwargs={
                'pk': beer_id})

    def render_to_response(self, context, **response_kwargs):
        print(context)
        beer_id = context['object'].id
        beer_detail_url = reverse(
            'beer:BeerDetail',
            kwargs={'pk': beer_id})
        return redirect(
            to=beer_detail_url)

class UpdateVote(LoginRequiredMixin, UpdateView):
    form_class = VoteForm
    queryset = Vote.objects.all()

    def get_object(self, queryset=None):
        vote = super().get_object(queryset)
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied(
                'cannot change another '
                'users vote'
        )
        return vote
    
    def get_success_url(self):
        beer_id = self.object.beer.id
        return reverse(
            'beer:BeerDetail',
            kwargs={'pk': beer_id})

    def render_to_response(self, context, **response_kwargs):
        beer_id = context['object'].id
        beer_detail_url = reverse(
            'beer:BeerDetail',
            kwargs={'pk': beer_id})
        return redirect(
            to=beer_detail_url)

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