from django.shortcuts import render, redirect
from django.contrib.auth.models import User
#   from accounts.models import AdvUser
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.aggregates import Sum

from beers.models import Beer

# Create your views here.
def signup(request):
    if request.method == 'POST':
        print(request.POST['username'])
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                print(User.objects.all())
                return render(request, 'accounts/signup.html', {'error': 'Username has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                auth.login(request, user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error': 'Passwords must match'})
    else:
        return render(request,'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'username or password is incorect.'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')

@login_required
def dashboard(request):
    user_beers = Beer.objects.all_with_related_instances_and_score()
    user_beers = user_beers.filter(hunter=request.user.id)
    user_beers = user_beers.order_by('-score')
    total_count = user_beers.count()
    top_ten = user_beers.order_by('-score')
    top_ten = top_ten.exclude(score=None)
    top_ten = top_ten[:10]
    total_score = 0
    for beer in user_beers:
        if beer.score:
            total_score += beer.score
    context = {
        'user_beers': user_beers,
        'total_score': total_score,
        'total_count': total_count,
        'top_ten': top_ten
    }
    return render(request, 'accounts/dashboard.html', context)
