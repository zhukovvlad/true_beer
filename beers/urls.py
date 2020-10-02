from django.urls import path
from . import views

app_name = 'beer'
urlpatterns = [
    path('', views.BeerList.as_view(), name='BeerList'),
    path('search/', views.search, name="Search"),
    path('create/', views.BeerCreate.as_view(), name='Create'),
    path('<str:slug>/', views.BeerDetail.as_view(), name='BeerDetail'),
    path('<str:slug>/comment', views.BeerCommentCreate.as_view(), name='BeerComment'),
    path('<str:slug>/update/', views.BeerUpdate.as_view(), name='Update'),
    path('<str:slug>/delete/', views.BeerDelete.as_view(), name='Delete'),
    path('<int:beer_id>/vote', views.CreateVote.as_view(), name='CreateVote'),
    path('<int:beer_id>/vote/<int:pk>', views.UpdateVote.as_view(), name='UpdateVote'),
]