from django.shortcuts import redirect, render
from django.contrib.auth import login , logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_GET , require_POST
from saas_com.core.exceptions import ObjectNotFound ,  AlreadyExists , InvalidForm , FollowException , InvalidContentType
from saas_com.core.service import is_safe_url

# =================FORMS=================
from .forms import LoginForm
from report.forms import ReportForm

# =================SERVICES=============
from .service import UserService , FollowService , BookmarkService
from apps.service import ReviewService
user_service = UserService()
follow_service = FollowService()
review_service = ReviewService()
bookmark_service = BookmarkService()


def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        try:
            user = user_service.authenticated(form, request)
            login(request , user)
            messages.success(request, "You have been logged in successfully.")
            return redirect("home")
        except InvalidForm:
            messages.error(request, "Invalid form data.")
        except ObjectNotFound:
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
    except ObjectNotFound as e:
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
    except ObjectNotFound as e:
        messages.error(request, str(e))
    except FollowException as e:
        messages.error(request, str(e))
    return redirect(HTTP_REFERER)


@require_GET
def view_profile(request , username):
    profile = user_service.repo.view_profile(username)
    form = ReportForm()
    return render(request , "profile.html" , {"profile":profile , "form":form})

@require_GET
def users(request , user_type):
    context = {}
    context["user_type"] = user_type.capitalize()
    context["users"] = user_service.get_users(user_type = user_type)
    return render(request , "users.html" , context)

@login_required(login_url = "login")
@require_POST
def add_bookmark(request , content_type , object_id):
    HTTP_REFERER = is_safe_url(request.META.get("HTTP_REFERER") , allowed_hosts = request.get_host())
    try:
        bookmark_service.add_bookmark(user = request.user , content_type = content_type , object_id = object_id)
        messages.success(request , f"This {content_type} is added to your bookmark")

    except InvalidContentType as e:
        messages.error(request , str(e))
    
    except AlreadyExists as e:
        messages.info(request , str(e))
    return redirect(HTTP_REFERER)

@login_required(login_url = "login")
@require_POST
def del_bookmark(request  , id):
    HTTP_REFERER = is_safe_url(request.META.get("HTTP_REFERER") , allowed_hosts = request.get_host())
    try:
        bookmark_service.delete_bookmark(user = request.user  , id = id)
        messages.success(request , f"Bookmarked removed")

    except ObjectNotFound as e:
        messages.error(request , str(e))
    
    return redirect(HTTP_REFERER)