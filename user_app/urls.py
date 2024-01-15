from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.register, name='register'),
    path('', views.login, name='login'),
]