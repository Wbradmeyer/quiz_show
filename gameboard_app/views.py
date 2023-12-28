from django.shortcuts import render

# Create your views here.
def select_board(request):
    return render(request, 'select_board.html')