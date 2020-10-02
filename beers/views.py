# from git

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied, ValidationError
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max, Count

from beers.models import Beer, Vote, BeerComment
from hops.models import Hop
from .forms import BeerCreateForm, BeerUpdateForm, VoteForm, BeerCommentForm

# Create your views here.
def home(request):
    qs = Beer.objects.all_with_related_instances_and_score()

    top_rating = qs.aggregate(Max('score'))
    top_beer = qs.filter(score=top_rating['score__max'])

    top_ibu = qs.aggregate(Max('ibu'))
    top_ibu_beer = qs.filter(ibu=top_ibu['ibu__max'])

    qs_hop = Hop.objects.all_with_prefetch_beers().annotate(count_beers=Count('used_hops'))
    qs_hop_max = qs_hop.aggregate(Max('count_beers'))
    top_hop = qs_hop.filter(count_beers=qs_hop_max['count_beers__max'])


    context = {
        'home': 'HOME PAGE',
        'max_score': top_rating['score__max'],
        'top_beer': top_beer,
        'top_ibu': top_ibu['ibu__max'],
        'top_ibu_beer': top_ibu_beer,
        'qs_hop_max': qs_hop_max['count_beers__max'],
        'top_hop': top_hop
    }

    return render(request, 'beers/home.html', context)

class BeerList(ListView):
    paginate_by = 10
    # model = Beer
    queryset = Beer.objects.all_with_related_instances_and_score()

    context_object_name = 'beer_list'

    ordering = ['-score']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['total_beer_list'] = Beer.objects.all()
        return context

class BeerDetail(DetailView):
    queryset = Beer.objects.all_with_related_instances_and_score()
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            beer_comment = BeerComment(
                beer=self.object,
                author=self.request.user
            )

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
            beer_comment_form = BeerCommentForm(instance=beer_comment)
            ctx['vote'] = vote
            ctx['vote_form'] = vote_form
            ctx['vote_form_url'] = vote_form_url
            ctx['beer_comment_form'] = beer_comment_form
        return ctx


class CreateVote(LoginRequiredMixin, CreateView):
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['beer'] = self.kwargs['beer_id']
        return initial
    
    def get_success_url(self):
        beer_slug = self.object.beer.slug
        try:
            return reverse(
                'beer:BeerDetail',
                kwargs={
                    'slug': beer_slug})
        except:
            raise ValidationError("Oooops")


    def render_to_response(self, context, **response_kwargs):
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
    form_class = BeerUpdateForm
    template_name = 'beers/update_view.html'

    def get_object(self, queryset=None):
        updated_beer = super().get_object(queryset)
        print(f"We update {updated_beer}")
        user = self.request.user
        if updated_beer.hunter != user:
            raise PermissionDenied("You can not change another user's beer")
        return updated_beer


class BeerDelete(LoginRequiredMixin, DeleteView):
    queryset = Beer.objects.all()
    #form_class = BeerCreateForm
    #template_name = 'beers/update_view.html'
    success_url = reverse_lazy('user:dashboard')

    def get_object(self, queryset=None):
        deleted_beer = super().get_object(queryset)
        user = self.request.user
        if deleted_beer.hunter != user:
            raise PermissionDenied("You can not delete another user's beer")
        return deleted_beer


class BeerCommentCreate(LoginRequiredMixin, CreateView):
    model = BeerComment
    form_class = BeerCommentForm

    def get_initial(self):
        initial = super().get_initial()
        initial['author'] = self.request.user.id
        initial['beer'] = self.kwargs['slug']
        return initial

    def get_success_url(self):
        beer_slug = self.object.beer.slug
        return reverse(
            'beer:BeerDetail',
            kwargs={'slug': beer_slug})
    
    '''def render_to_response(self, context, **response_kwargs):
        print('Context for vote is ', context)
        beer_id = context['object'].id
        beer_detail_url = reverse(
            'beer:BeerDetail',
            kwargs={'pk': beer_id})
        return redirect(
            to=beer_detail_url)'''


def q():
    return 5


def search(request):
    if request.method == 'POST':
        queryset = Beer.objects.all_with_related_instances_and_score()
        for i in queryset:
            print(i)
        search_item = request.POST['q'].lower()
        print(f'We are looking for {search_item}')
        if not search_item:
            return render(request, 'beers/search_result.html')
        search_result = [item for item in queryset if search_item in item.title]
        return render(request, 'beers/search_result.html', {
            'entries': search_result
        })
    else:
        return render(request, 'beers/search_result.html')