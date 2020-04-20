from django.urls import path
from . import views

app_name = 'beer'
urlpatterns = [
    path('', views.BeerList.as_view(), name='BeerList'),
    path('create', views.BeerCreate.as_view(), name='Create'),
    path('<str:slug>', views.BeerDetail.as_view(), name='BeerDetail'),
    path('<str:slug>/update/', views.BeerUpdate.as_view(), name='Update'),
    path('<int:beer_id>/vote', views.CreateVote.as_view(), name='CreateVote'),
    path('<int:beer_id>/vote/<int:pk>', views.UpdateVote.as_view(), name='UpdateVote'),
]