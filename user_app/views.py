from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    return redirect('/')

def login(request):
    return  redirect('/')