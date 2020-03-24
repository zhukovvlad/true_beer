from django.urls import path
from . import views

app_name = 'hop'
urlpatterns = [
    path('', views.HopList.as_view(), name='HopList'),
    path('<int:pk>', views.HopDetail.as_view(), name='HopDetail'),
]