from django.shortcuts import render, redirect
from django.contrib import messages
from . models import User
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if 'email_error' in request.session:
        del request.session['email_error']
    if 'password_error' in request.session:
        del request.session['password_error']
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(hashedpw)
        registered_user = User.objects.create(first_name = request.POST['first_name'],
                                            last_name = request.POST['last_name'],
                                            email = request.POST['email'],
                                            password = hashedpw)
        request.session['user_id'] = registered_user.id
        return redirect('/games')

def login(request):
    if 'email_error' in request.session:
        del request.session['email_error']
    if 'password_error' in request.session:
        del request.session['password_error']
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/games')
        else:
            request.session['password_error'] = 'This password does not match our records.'
            return redirect('/')
    else:
        request.session['email_error'] = 'This email does not match our records.'
    return redirect('/')

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('/')