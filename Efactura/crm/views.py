from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, AddRecordForm
from .models import Record

def crmhome(request):
    return render(request, "crmhome.html", {})

def crmlogin(request):
        # Check if logged în
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try: 
            dbuser = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"User {username} has been logged in!")
            context = {'user': user}
            return redirect('crmindex')
        else:
            messages.error(request, "Error logging in!")
            return redirect('crmindex')
    else:
        return render(request, "crmlogin.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, "User has been logged out...")
    return redirect('crmindex')
    # return render(request, "crmindex.html", {})

def login_user(request):
    return redirect('crmlogin')
    # return render(request, "crmindex.html", {})

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('crmindex')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})

    return render(request, 'register.html', {'form':form})