from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_select_board, name='main_select'),
    path('select', views.select_gameboard, name='select_game'),
    path('new', views.create_game, name='new_game'),
    # path('update/<int:game_id>', views.edit_game),
    path('delete/<int:game_id>', views.delete_game, name='delete_game'),
    path('play/<int:game_id>', views.play_gameboard, name='play'),
    path('categories', views.display_categories, name='show_cats'),
    path('categories/new', views.create_category, name='new_cat'),
    path('categories/<int:cat_id>', views.display_cat_questions, name='show_cat_qs'),
    # path('categories/update/<int:cat_id>', views.edit_category),
    path('categories/delete/<int:cat_id>', views.delete_category, name='delete_cat'),
    path('questions/new', views.create_question, name='new_question'),
    path('questions/<int:question_id>', views.display_question, name='show_ques'),
    path('questions/edit/<int:question_id>', views.question_edit_page, name='edit_ques_page'),
    path('questions/update', views.edit_question, name='edit_ques'),
    path('questions/delete/<int:question_id>', views.delete_question, name='delete_ques'),
]