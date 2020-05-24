from django.urls import path
from . import views

app_name = 'brewery'
urlpatterns = [
    path('', views.BreweryList.as_view(), name='BreweryList'),
    path('create/', views.BreweryCreate.as_view(), name='Create'),
    path('<str:slug>', views.BreweryDetail.as_view(), name='BreweryDetail'),
]