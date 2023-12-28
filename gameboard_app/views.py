from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return redirect('/games/new')

def select_board(request):
    return render(request, 'select_gameboard.html')

def display_question(request):
    return render(request, 'question.html')

def play_gameboard(request):
    return render(request, 'gameboard.html')