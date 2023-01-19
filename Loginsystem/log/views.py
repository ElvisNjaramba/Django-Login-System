from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
def index(request):
    context = {}
    return render(request, 'log\index.html', context)

def home(request):
    context = {}
    return render(request, 'log\home.html', context)

def signup(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if User.objects.filter(username=username):
            messages.error(request, "Username exists.")
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, "Email exists.")
            return redirect('signup')

        if pass2 != pass1:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        my_user = User.objects.create_user(username, email, pass1)
        my_user.phone_number = phone
        my_user.first_name = fname
        my_user.last_name = lname
        my_user.save()
        messages.success(request, 'Your account has successfully been created.')

        return redirect('signin')
    context = {}
    return render(request, 'log\signup.html', context)

def signin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user = authenticate(username=username, password = pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            context = {'fname':fname}
            return render(request, 'log\home.html', context)

        else :
            messages.error(request, "Check your login info!!")
            return redirect('signin')

    return render(request, 'log\signin.html')


def signout(request):
    logout(request)
    messages.success(request, 'You logged out successfully')
    return redirect('index')