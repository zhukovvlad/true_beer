from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Hop

# Create your views here.

class HopList(ListView):
    model = Hop

class HopDetail(DetailView):
    model = Hop