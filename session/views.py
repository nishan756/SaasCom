from django.shortcuts import redirect, render
from django.contrib.auth import login , logout , authenticate
from django.contrib import messages
from django.views.decorators.http import require_GET , require_POST
from .exceptions import InvalidForm , UserNotFound

# =================FORMS=================
from .forms import LoginForm

# =================SERVICES=============
from .service import UserService
user_service = UserService()


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        try:
            user = user_service.authenticated(form, request)
            login(request , user)
            messages.success(request, "You have been logged in successfully.")
            return redirect("home")
        except InvalidForm:
            messages.error(request, "Invalid form data.")
        except UserNotFound:
            messages.error(request, "Invalid username or password.")
        return redirect("login")
    else:
        form = LoginForm()
    
    return render(request , "login.html" , {"form":form})


def user_logout(request):
    logout(request)
    messages.success(request , "You have been logged out successfully.")
    return redirect("home")