from django.shortcuts import redirect, render
from django.contrib.auth import login , logout , authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_GET , require_POST
from .exceptions import InvalidForm , UserNotFound , FollowException , InvalidContentType
from apps.views import is_safe_url

# =================FORMS=================
from .forms import LoginForm , ReportForm

# =================SERVICES=============
from .service import UserService , FollowService , ReportService
user_service = UserService()
follow_service = FollowService()
report_service = ReportService()


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

@login_required(login_url = "login")
@require_GET
def user_logout(request):
    logout(request)
    messages.success(request , "You have been logged out successfully.")
    return redirect("home")


@login_required(login_url = "login")
@require_POST
def follow(request , id):
    HTTP_REFERER = is_safe_url(request.META.get("HTTP_REFERER") , allowed_hosts=request.get_host())
    following_user = user_service.repo.get_user(id)
    follower = request.user
    try:
        follow_service.follow(follower, following_user)
        messages.success(request, f"You have started following {following_user.full_name()}.")
    except UserNotFound as e:
        messages.error(request, str(e))
    except FollowException as e:
        messages.error(request, str(e))
    return redirect(HTTP_REFERER)

@login_required(login_url = "login")
@require_POST
def unfollow(request , id):
    HTTP_REFERER = is_safe_url(request.META.get("HTTP_REFERER") , allowed_hosts=request.get_host())
    following_user = user_service.repo.get_user(id)
    follower = request.user
    try:
        follow_service.unfollow(follower, following_user)
        messages.success(request, f"You have unfollowed {following_user.full_name()}.")
    except UserNotFound as e:
        messages.error(request, str(e))
    except FollowException as e:
        messages.error(request, str(e))
    return redirect(HTTP_REFERER)


@require_GET
def view_profile(request , username):
    profile = user_service.repo.view_profile(username)
    form = ReportForm()
    return render(request , "profile.html" , {"profile":profile , "form":form})

@require_POST
@login_required(login_url = "login")
def report(request , content_type , id):
    HTTP_REFERER = is_safe_url(request.META.get("HTTP_REFERER") , allowed_hosts=request.get_host())
    try:
        report_service.add_report(reporter=request.user, content_type=content_type, id=id, form=ReportForm(request.POST))
        messages.success(request, "Your report has been submitted successfully.")

    except InvalidContentType as e:
        messages.error(request, str(e))
    
    except InvalidForm as e:
        messages.error(request, str(e))
    
    except Exception as e:
        messages.error(request, "An error occurred while submitting your report. Please try again later.")
    return redirect(HTTP_REFERER)