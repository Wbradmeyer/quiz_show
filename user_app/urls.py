from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/new', views.register, name='register'),
    path('users/login', views.login, name='login'),
    path('users/logout', views.logout, name='logout'),
]