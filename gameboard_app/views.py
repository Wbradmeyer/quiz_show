from django.shortcuts import render, redirect
from . models import Game, Category, Question

# Create methods
def create_game(request):
    game = Game.add_game({'title': request.POST['title']})
    request.session['game_id'] = game.id
    return redirect('/games/categories')

def create_category(request):
    game = Game.get_by_id(request.POST['game_id'])
    Category.add_category({'name': request.POST['name'], 'game_assigned': game})
    return redirect('/games/categories')

def create_question(request):
    category = Category.get_by_id(request.POST['cat_id'])
    Question.add_question({'question': request.POST['question'], 'answer': request.POST['answer'],
                        'points': request.POST['points'], 'category_assigned': category})
    return redirect(f'/games/categories/{category.id}')

# Read methods
def index(request):
    return redirect('/games')

def display_select_board(request):
    if 'game_id' in request.session:
        del request.session['game_id']
    content = {
        'all_games': Game.get_all()
    }
    return render(request, 'select_gameboard.html', content)

def select_gameboard(request):
    if request.POST['game_id'] == '0':
        return redirect('/games')
    request.session['game_id'] = request.POST['game_id']
    return redirect('/games/categories')

def display_categories(request):
    content = {
        'game': Game.get_by_id(request.session['game_id']),
    }
    return render(request, 'categories.html', content)

def display_cat_questions(request, cat_id):
    content = {
        'category': Category.get_by_id(cat_id),
    }
    return render(request, 'new_question.html', content)

def display_question(request, question_id):
    question = Question.get_by_id(id=question_id)
    content = {
        'question': question,
        'category': question.category_assigned
    }
    return render(request, 'question.html', content)

def play_gameboard(request, game_id):
    game = Game.get_by_id(id=game_id)
    content = {
        'game': game,
        'categories': game.categories_avail.all()
    }
    return render(request, 'gameboard.html', content)

# Update methods
# def edit_game(request, game_id):
#     Game.update({'id':game_id, 'title':request.POST['title']})
#     return redirect('/games/categories')

# def edit_category(request, cat_id):
#     Category.update({'id':cat_id, 'name':request.POST['name']})
#     return redirect(f'/games/categories/{cat_id}')

def question_edit_page(request, question_id):
    question = Question.get_by_id(id=question_id)
    content = {
        'question': question,
        'category': question.category_assigned
    }
    return render(request, 'edit_question.html', content)

def edit_question(request):
    Question.update({'id':request.POST['question_id'], 'question':request.POST['question'], 
                    'answer':request.POST['answer'], 'points':request.POST['points']})
    return redirect(f"/games/questions/{request.POST['question_id']}")

# Delete methods
def delete_game(request, game_id):
    Game.destroy(id=game_id)
    return redirect('/games')

def delete_category(request, cat_id):
    Category.destroy(id=cat_id)
    return redirect('/games/categories')

def delete_question(request, question_id):
    category = Question.get_by_id(id=question_id).category_assigned
    Question.destroy(id=question_id)
    return redirect(f'/games/categories/{category.id}')