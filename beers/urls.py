from django.urls import path
from . import views

app_name = 'beer'
urlpatterns = [
    path('', views.BeerList.as_view(), name='BeerList'),
    path('beer/<int:pk>', views.BeerDetail.as_view(), name='BeerDetail'),
]