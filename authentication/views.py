from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from chat_core.models import Bots


def signup_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect("home_view")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            messages.error(request, "passwords don't match")
            return redirect("signup_view")
        myuser = User(username=username)
        myuser.set_password(password)
        myuser.save()
        login(request, myuser)
        messages.success(request, "account created successfully")
        return redirect("home_view")
    return render(request, "signup.html")


def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect("home_view")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user_authentication = authenticate(
            request, username=username, password=password
        )
        if not user_authentication is None:
            login(request, user_authentication)
            messages.success(request, "login successful")
            return redirect("home_view")
        else:
            messages.error(request, "invalid credentials")
            return redirect("login_view")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login_view")


def home_view(request):
    user = request.user
    username = user.username
    if not user.is_authenticated:
        return redirect("login_view")
    bots = []
    bots_exist = True
    bots_getter = Bots.objects.filter(user = user)
    for bot in bots_getter:
        bots.append(bot)
    if len(bots) == 0:
        bots_exist = False
    return render(request, "home.html", {"bots" : bots, "bots_exist" : bots_exist, "username" : username})