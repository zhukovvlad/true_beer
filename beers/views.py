# from git

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
    # print ('Queryset is ', queryset.values())

    context_object_name = 'beer_list'

class BeerDetail(DetailView):
    queryset = Beer.objects.all_with_related_instances_and_score()
    
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
        print('KWARGS are ', self.kwargs)
        initial['user'] = self.request.user.id
        initial['beer'] = self.kwargs['beer_id']
        print('final initial is ', initial)
        return initial
    
    def get_success_url(self):
        beer_slug = self.object.beer.slug
        return reverse(
            'beer:BeerDetail',
            kwargs={
                'slug': beer_slug})

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
        beer_slug = self.object.beer.slug
        return reverse(
            'beer:BeerDetail',
            kwargs={'slug': beer_slug})

    def render_to_response(self, context, **response_kwargs):
        beer_id = context['object'].id
        beer_detail_url = reverse(
            'beer:BeerDetail',
            kwargs={'pk': beer_id})
        return redirect(
            to=beer_detail_url)


class BeerCreate(LoginRequiredMixin, CreateView):
    form_class = BeerCreateForm
    template_name = 'beers/create.html'

    def get_initial(self):
        return {
            'hunter': self.request.user.id
        }

class BeerUpdate(LoginRequiredMixin, UpdateView):
    queryset = Beer.objects.all()
    form_class = BeerCreateForm
    template_name = 'beers/update_view.html'
    print(object)
