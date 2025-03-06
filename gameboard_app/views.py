from django.shortcuts import render, redirect
from django.contrib import messages
from . models import Game, Category, Question
from . forms import UploadFileForm

# Create methods
def create_game(request):
    errors = Game.objects.game_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/games')
    game = Game.add_game({'title': request.POST['title'], 'user_id': request.session['user_id']})
    request.session['game_id'] = game.id
    return redirect('/games/categories')

def create_category(request):
    errors = Category.objects.category_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/games/categories')
    game = Game.get_by_id(request.POST['game_id'])
    Category.add_category({'name': request.POST['name'], 'game_assigned': game})
    return redirect('/games/categories')

def create_question(request):
    # add validations here
    errors = Question.objects.question_validator(request.POST)
    if len(errors) > 0:
        cat_id = request.POST['cat_id']
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/games/categories/{cat_id}')
    category = Category.get_by_id(request.POST['cat_id'])
    file_form = UploadFileForm(request.POST, request.FILES)
    Question.add_question({'question': request.POST['question'], 
                        'answer': request.POST['answer'],
                        'points': request.POST['points'], 
                        'category_assigned': category, 
                        # 'file': file_form})
                        'pic': file_form})
    return redirect(f'/games/categories/{category.id}')

def add_player(request):
    game = Game.get_by_id(request.POST['game_id'])
    if 'player_1' not in request.session:
        request.session['player_1'] = request.POST['player_name']
        request.session['score_1'] = 0
        request.session['player_count'] = 1
    elif 'player_2' not in request.session:
        request.session['player_2'] = request.POST['player_name']
        request.session['score_2'] = 0
        request.session['player_count'] += 1
        request.session['turn'] = 1
    return redirect(f'/games/play/{game.id}')

def answer_question(request):
    question = Question.get_by_id(request.POST['question_id'])
    if question.answer.lower() == request.POST['answer'].lower():
        return redirect(f'/games/questions/correct/{question.id}')
    return redirect(f'/games/questions/incorrect/{question.id}')


# Read methods
def display_select_board(request):
    Question.reset_all_questions()
    if 'user_id' not in request.session:
        return redirect('/')
    # clear all session items associated with playing a game
    if 'game_id' in request.session:
        Game.update_activity({'id': request.session['game_id'], 'is_active': False})
        del request.session['game_id']
    if 'player_1' in request.session:
        del request.session['player_1']
    if 'score_1' in request.session:
        del request.session['score_1']
    if 'player_2' in request.session:
        del request.session['player_2']
    if 'score_2' in request.session:
        del request.session['score_2']
    if 'player_count' in request.session:
        del request.session['player_count']
    if 'turn' in request.session:
        del request.session['turn']
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
        'user_id': request.session['user_id'],
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
    game = Game.get_by_id(game_id)
    categories = game.categories_avail.all()
    game_over = True
    # track the leader/winner
    leader = ''
    if 'player_count' in request.session and request.session['player_count'] == 2:
        if request.session['score_1'] > request.session['score_2']:
            leader = request.session['player_1']
        elif request.session['score_2'] > request.session['score_1']:
            leader = request.session['player_2']
        else:
            leader = "It's a tie."

    if not game.is_active:
        game.update_activity({'id': game_id, 'is_active': True})
    # if there are any questions left, the game is not over
    for category in categories:
        if category.question_list.filter(played=False):
            game_over = False
    context = {
        'game': game,
        'categories': categories,
        'game_over': game_over,
        'winner': leader
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
    if 'turn' in request.session and request.session['turn'] == 2:
        request.session['score_2'] += question.points
    else:
        request.session['score_1'] += question.points
    game = Game.get_by_id(request.session['game_id'])
    return redirect(f'/games/play/{game.id}')

def incorrect_answer(request, question_id):
    question = Question.get_by_id(question_id)
    # only change turns if player count is 2
    if request.session['player_count'] == 2:
        if request.session['turn'] == 1:
            request.session['turn'] += 1
        elif request.session['turn'] == 2:
            request.session['turn'] -= 1
        print(request.session['turn'])
        if not question.played:
            question.update_played({'id': question.id, 'played': True})
            return redirect(f'/games/questions/{question.id}')
        game = Game.get_by_id(request.session['game_id'])
        return redirect(f'/games/play/{game.id}')
    else:
        question.update_played({'id': question.id, 'played': True})
        game = Game.get_by_id(request.session['game_id'])
        return redirect(f'/games/play/{game.id}')


# Delete methods
def delete_game(request, game_id):
    game = Game.get_by_id(id=game_id)
    # only allow if session user created game AND is logged in
    if 'user_id' not in request.session or game.creator.id != request.session['user_id']:
        return redirect('/')
    del request.session['game_id']
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