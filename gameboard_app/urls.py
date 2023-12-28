from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('select', views.select_board),
    path('play', views.play_gameboard),
    path('categories', views.display_categories),
    # path('categories/new', views.add_category),
    # path('/questions/<int:question_id>', views.display_question),
    path('questions', views.display_question),
]