from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('new', views.select_board),
    path('play', views.play_gameboard),
    # path('/questions/<int:question_id>', views.display_question),
    path('questions/', views.display_question),
]