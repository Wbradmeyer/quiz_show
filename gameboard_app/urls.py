from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_select_board),
    path('select', views.select_gameboard),
    path('new', views.create_game),
    path('delete/<int:game_id>', views.delete_game),
    path('play', views.play_gameboard),
    path('categories', views.display_categories),
    path('categories/new', views.create_category),
    path('categories/<int:cat_id>', views.display_cat_questions),
    path('categories/delete/<int:cat_id>', views.delete_category),
    path('questions/new', views.create_question),
    path('questions/<int:question_id>', views.display_question),
    path('questions/delete/<int:question_id>', views.delete_question),
]