from django.shortcuts import render, redirect
from . models import Game, Category, Question

# Create methods
def create_game(request):
    game = Game.add_game({'title': request.POST['title'], 'user_id': request.session['user_id']})
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

def add_player(request):
    game = Game.get_by_id(request.POST['game_id'])
    request.session['player_1'] = request.POST['player_name']
    request.session['score_1'] = 0
    return redirect(f'/games/play/{game.id}')

# Read methods
def display_select_board(request):
    Question.reset_all_questions()
    if 'user_id' not in request.session:
        return redirect('/')
    if 'game_id' in request.session:
        Game.update_activity({'id': request.session['game_id'], 'is_active': False})
        # print(game.is_active)
        del request.session['game_id']
    if 'player_1' in request.session:
        del request.session['player_1']
    context = {
        'all_games': Game.get_all()
    }
    return render(request, 'select_gameboard.html', context)

def select_gameboard(request):
    if request.POST['game_id'] == "0":
        return redirect('/games')
    request.session['game_id'] = request.POST['game_id']
    return redirect('/games/categories')

def display_categories(request):
    if 'user_id' not in request.session or 'game_id' not in request.session:
        return redirect('/')
    # only allow if session user created game
    game = Game.get_by_id(request.session['game_id'])
    context = {
        'game': game,
    }
    return render(request, 'categories.html', context)

def display_cat_questions(request, cat_id):
    if 'user_id' not in request.session or 'game_id' not in request.session:
        return redirect('/')
    # only allow if session user created game
    category = Category.get_by_id(cat_id)
    if category.game_assigned.creator.id != request.session['user_id']:
        return redirect('/games')
    context = {
        'category': Category.get_by_id(cat_id),
    }
    return render(request, 'new_question.html', context)

def display_question(request, question_id):
    if 'user_id' not in request.session:
        return redirect('/')
    question = Question.get_by_id(id=question_id)
    context = {
        'question': question,
        'category': question.category_assigned
    }
    return render(request, 'question.html', context)

def play_gameboard(request, game_id):
    if 'user_id' not in request.session:
        return redirect('/')
    game = Game.update_activity({'id': game_id, 'is_active': True})
    # print(game.is_active)
    # print(request.session['game_id'])
    context = {
        'game': game,
        'categories': game.categories_avail.all()
    }
    return render(request, 'gameboard.html', context)

# Update methods
# def edit_game(request, game_id):
#     Game.update({'id':game_id, 'title':request.POST['title']})
#     return redirect('/games/categories')

# def edit_category(request, cat_id):
#     Category.update({'id':cat_id, 'name':request.POST['name']})
#     return redirect(f'/games/categories/{cat_id}')

def question_edit_page(request, question_id):
    if 'user_id' not in request.session or 'game_id' not in request.session:
        return redirect('/')
    # only allow if session user created game
    question = Question.get_by_id(id=question_id)
    if question.category_assigned.game_assigned.creator.id != request.session['user_id']:
        return redirect('/games')
    context = {
        'question': question,
        'category': question.category_assigned
    }
    return render(request, 'edit_question.html', context)

def edit_question(request):
    Question.update({'id':request.POST['question_id'], 'question':request.POST['question'], 
                    'answer':request.POST['answer'], 'points':request.POST['points']})
    return redirect(f"/games/questions/{request.POST['question_id']}")

def correct_answer(request, question_id):
    question = Question.get_by_id(question_id)
    question.update_played({'id': question.id, 'played': True})
    request.session['score_1'] += question.points
    game = Game.get_by_id(request.session['game_id'])
    return redirect(f'/games/play/{game.id}')

def incorrect_answer(request, question_id):
    question = Question.get_by_id(question_id)
    question.update_played({'id': question.id, 'played': True})
    game = Game.get_by_id(request.session['game_id'])
    return redirect(f'/games/play/{game.id}')

# Delete methods
def delete_game(request, game_id):
    game = Game.get_by_id(id=game_id)
    # only allow if session user created game AND is logged in
    if 'user_id' not in request.session or game.creator.id != request.session['user_id']:
        return redirect('/')
    Game.destroy(id=game_id)
    return redirect('/games')

def delete_category(request, cat_id):
    category = Category.get_by_id(id=cat_id)
    # only allow if session user created game AND is logged in
    if 'user_id' not in request.session or category.game_assigned.creator.id != request.session['user_id']:
        return redirect('/')
    Category.destroy(id=cat_id)
    return redirect('/games/categories')

def delete_question(request, question_id):
    category = Question.get_by_id(id=question_id).category_assigned
    # only allow if session user created game AND is logged in
    if 'user_id' not in request.session or category.game_assigned.creator.id != request.session['user_id']:
        return redirect('/')
    Question.destroy(id=question_id)
    return redirect(f'/games/categories/{category.id}')