from django.shortcuts import render , redirect

# ===================MODELS================
from .models import App
# ====================SERVICES=============
from .service import AppService , VoteService , AppImageService , ReviewService
from django.contrib import messages
from django.views.decorators.http import require_GET , require_POST
from django.contrib.auth.decorators import login_required

# ==================EXCEPTIONS=============
from .exceptions import AlreadyReviewed , AppNotFound
from session.exceptions import UserNotFound

# =================FORMS=================
from .forms import ReviewForm



# =========SERVICES=========
app_service = AppService()
vote_service = VoteService()
app_image_service = AppImageService()
review_service = ReviewService()

def home(request):
    return render(request , "index.html")

def all_apps(request):
    order_by = request.GET.get("order_by" , None)
    context = {}
    context["apps"] = app_service.all_apps(order_by = order_by)
    return render(request , "apps.html" , context)

def app_detail(request , id):
    context = {}
    context["app"] = app_service.get_app(id = id)
    context["images"] = app_image_service.get_images(id)
    context["user_vote"] = vote_service.has_vote(context["app"], request.user)
    context["form"] = ReviewForm()
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


def add_review(request , id):
    try:
        msg = review_service.add_review(app_id = id , user = request.user)["msg"]
        messages.success(request , msg)
    except AlreadyReviewed as e:
        return messages.info(request , str(e))
    return redirect("app-detail" , id = id)    

