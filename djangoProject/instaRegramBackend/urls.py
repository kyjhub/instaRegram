from django.urls import path
from . import views


urlpatterns = [
    path('instaRegram/', views.temp_here, name='temp_here'),
    path('instaRegram/urlinput', views.instaCrawling, name='instaCrawling'),
]