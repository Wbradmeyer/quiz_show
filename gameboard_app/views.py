from django.shortcuts import render, redirect
from . models import Game, Category, Question

# Create methods
def create_game(request):
    Game.add_game({'title': request.POST['title']})
    return redirect('/games/categories')

def create_category(request):
    game = Game.get_by_id(request.POST['game_id'])
    Category.add_category({'name': request.POST['name'], 'game_assigned': game})
    return redirect('/games/categories')

def create_question(request):
    category = Category.get_by_id(request.POST['cat_id'])
    Question.add_question({'question': request.POST['question'], 'answer': request.POST['answer'],
                        'points': request.POST['points'], 'category_assigned': category})
    return redirect('/games/questions')

# Read methods
def index(request):
    return redirect('/games/select')

def display_select_board(request):
    content = {
        'all_games': Game.get_all()
    }
    return render(request, 'select_gameboard.html', content)

def select_gameboard(request):
    game = Game.get_by_id(id=request.POST['game_id'])
    request.session['active_game'] = game
    return redirect('games/categories')

def display_categories(request):
    content = {
        'all_categories': Category.get_all(),
        # want a list of game's cats
    }
    return render(request, 'categories.html', content)

def display_cat_questions(request):
    content = {
        'all_questions': Question.get_all(),
        # want a list of cat's ques
    }
    return render(request, 'new_question.html')

def display_question(request):
    return render(request, 'question.html')

def play_gameboard(request):
    return render(request, 'gameboard.html')

# Update methods


# Delete methods