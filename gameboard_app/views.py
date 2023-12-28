from django.shortcuts import render, redirect

# Create methods


# Read methods
def index(request):
    return redirect('/games/select')

def select_board(request):
    return render(request, 'select_gameboard.html')

def display_categories(request):
    return render(request, 'categories.html')

def display_cat_questions(request):
    return render(request, 'new_question.html')

def display_question(request):
    return render(request, 'question.html')

def play_gameboard(request):
    return render(request, 'gameboard.html')

# Update methods


# Delete methods