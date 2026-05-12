from django.shortcuts import render , redirect
from django.utils.http import url_has_allowed_host_and_scheme

# ===================MODELS================
from .models import App
# ====================SERVICES=============
from .service import AppService , VoteService , AppImageService , ReviewService
from session.service import FollowService , UserService
from django.contrib import messages
from django.views.decorators.http import require_GET , require_POST
from django.contrib.auth.decorators import login_required

# ==================EXCEPTIONS=============
from .exceptions import AlreadyReviewed , AppNotFound, PermissionDenied
from session.exceptions import UserNotFound

# =================FORMS=================
from .forms import ReviewForm



# =========SERVICES=========
app_service = AppService()
vote_service = VoteService()
app_image_service = AppImageService()
review_service = ReviewService()
user_service = UserService()
follow_service = FollowService()

def is_safe_url(url , allowed_hosts):
    if url_has_allowed_host_and_scheme(url , allowed_hosts = allowed_hosts):
        return url
    return "/"

@require_GET
def home(request):
    return render(request , "index.html")


@require_GET
def all_apps(request):
    order_by = request.GET.get("order_by" , None)
    context = {}
    context["apps"] = app_service.all_apps(order_by = order_by)
    return render(request , "apps.html" , context)

@require_GET
def app_detail(request , id):
    context = {}
    context["app"] = app_service.get_app_detail(id = id)
    context["user_vote"] = vote_service.has_vote(context["app"], request.user)
    context["form"] = ReviewForm()
    context["user_vote"] = vote_service.has_vote(context["app"], request.user) if request.user.is_authenticated else None
    context["is_following"] = follow_service.is_following(request.user, context["app"].founder) if request.user.is_authenticated else False
    return render(request , "app-detail.html" , context)

@require_POST
@login_required(login_url = "login")
def vote(request , id):
    vote_type = request.POST.get("vote_type")
    try:
        msg = vote_service.vote(app_id = id , user = request.user , vote_type = vote_type)
        messages.success(request , msg)
    except AppNotFound as e:
        messages.error(request , message = e)
    return redirect("app-detail" , id)

@require_POST
@login_required(login_url = "login")
def add_review(request , id):
    try:
        review = request.POST.get("review")
        review_service.add_review(app_id = id , user = request.user , review = review)
        messages.success(request , "Thanks for your review!")
    except AlreadyReviewed as e:
        messages.info(request , str(e))
    return redirect("app-detail" , id = id)    

@require_POST
@login_required(login_url = "login")
def del_review(request , id):
    HTTP_REFERER = is_safe_url(request.META.get("HTTP_REFERER") , allowed_hosts = {request.get_host()})
    try:
        review_service.del_review(id = id , user = request.user)
        messages.success(request , "Review deleted successfully!")
    except PermissionDenied as e:
        messages.error(request , str(e))
    return redirect(HTTP_REFERER)    

