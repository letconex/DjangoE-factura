from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def crmindex(request):
    # return HttpResponse("Crm index.")
    # Check if logged în
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"User {username} has been logged!")
            context = {'user': user}
            return redirect('crmindex', context=context)
        else:
            messages.errors(request, "Error logging in!")
            return redirect('home')
    else:
        return render(request, "crmindex.html", {})

def login_user(request):
    pass
    # return render(request, "crmindex.html", {})

def logout_user(request):
    pass
    # return render(request, "crmindex.html", {})