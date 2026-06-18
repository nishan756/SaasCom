from django.shortcuts import render , redirect
from django.contrib import messages
from django.views.decorators.http import require_GET , require_POST
from django.contrib.auth.decorators import login_required
from saas_com.core.service import is_safe_url
from .models import Category
from django.db import transaction

# ====================SERVICES=============
from .service import AppService , AppImageService , ReviewService
from session.service import FollowService , UserService
from bookmark.service import BookmarkService
from report.service import ReportService
from vote.service import VoteService
from discussion.service import DiscussionService

# ==================EXCEPTIONS=============
from saas_com.core.exceptions import AlreadyExists , ObjectNotFound, PermissionDenied , TooManyObject , InvalidForm , InvalidPassword

# =================FORMS=================
from .forms import ReviewForm , AppForm , AppDeletionConfirmationForm
from report.forms import ReportForm

# =========LOGGING==========
import logging
logger = logging.getLogger("apps")

# =========SERVICES=========
app_service = AppService()
vote_service = VoteService()
app_image_service = AppImageService()
review_service = ReviewService()
user_service = UserService()
follow_service = FollowService()
report_service = ReportService()
bookmark_service = BookmarkService()
discussion_service = DiscussionService()

@require_GET
def home(request):
    context = {
        "total_apps": app_service.total_apps(),
        "total_users": user_service.total_user(),
        "trending_apps":app_service.trending_apps(),
        "categories":Category.objects.all(),
        "trending_discussions":discussion_service.trending_discussions()
    }
    return render(request , "index.html" , context)


@require_GET
def all_apps(request):
    query_set = request.GET.dict()
    page = query_set.pop("page" , 1)
    context = {}
    context["apps"] = app_service.all_apps(page = page , **query_set)
    context["categories"] = Category.objects.all()
    return render(request , "apps.html" , context)

@require_GET
def app_detail(request , id):
    context = {}
    try:
        context["app"] = app_service.get_app_detail(id = id)

    except ObjectNotFound as e:
        messages.info(request , str(e))
        return redirect("all-apps")
    
    except Exception as e:
        messages.error(request , "Somethign went wrong")
        return redirect("home")
    # Checking if the user is authenticated 
    if request.user.is_authenticated:
        context["user_vote"] = vote_service.get_vote(user = request.user , content_type_str = 'app' , object_id = id)
        context["is_following"] = follow_service.is_following(follower = request.user , following = context["app"].user)
        context["user_report"] = report_service.has_user_report(content_type_str = "app" , object_id = id , reporter = request.user)
        context["bookmark"] = bookmark_service.is_bookmarked(user = request.user , content_type = 'app' , object_id = id)
    
    context["app_del_form"] = AppDeletionConfirmationForm()
    context["report_form"] = ReportForm()
    context["form"] = ReviewForm()
    context["rating_range"] = range(5)
    return render(request , "app-detail.html" , context)

@login_required(login_url = "login")
def create_app(request):
    if request.method == "POST":
        form = AppForm(request.POST , request.FILES)
        try:
            if form.is_valid():
                with transaction.atomic():
                    new_app = app_service.create_app(user = request.user , form = form)
                    images = request.FILES.getlist("images")
                    if images:
                        app_image_service.add_images(app = new_app , images = images)
                    logger.info(f"{request.user} created {new_app.name}")
                return redirect("app-detail" , id = new_app.id)
            else:
                logger.error(msg = f"Invalid form of : {request.user}->Errors:{form.errors}")
                messages.error(request , form.errors)
        
        except TooManyObject as e:
            logger.info(msg = f"{request.user} tried to add more than 5 image")
            messages.info(request , str(e))
        
        except Exception as e:
            logger.exception(msg = f"{request.user} got an exception")
            messages.info(request , "Something went wrong. Please try again later")
    else:
        form = AppForm()

    return render(request , "create-app.html" , {"form":form , "instance":False})

@login_required(login_url = "login")
def update_app(request , id):
    app = app_service.get_app(id = id)
    context = {}
    context["form"] = AppForm(instance = app)
    context["instance"] = True
    if app.user != request.user:
        messages.warning(request , "Can't update this app")
        return redirect("app-detail" , id)
    
    if request.method == "POST":
        form = AppForm(instance = app , data = request.POST , files = request.FILES)
        images = request.FILES.getlist("images" , None)
        try:
            updated_app = app_service.update_app(form = form)
            if images:
                app_image_service.add_images(updated_app , images)
            return redirect("app-detail" , id)
        
        except InvalidForm as e:
            messages.error(request , str(e))
            return render(request , "create-app.html" , {"form":form})
        
        except TooManyObject as e:
            messages.info(request , str(e))
        
        except Exception as e:
            messages.info(request , "Something went wrong. Please try again later")
    return render(request , "create-app.html" , context)

@require_POST
@login_required(login_url = "login")
def del_app(request , id):
    HTTP_REFERER = is_safe_url(request.META.get("HTTP_REFERER" , "/") , request.get_host())
    form = AppDeletionConfirmationForm(data = request.POST)
    user= request.user
    try:
        app_service.del_app(id , user , form)
        messages.success(request , "Successfully deleted your app")
        return redirect("all-apps")
    
    except PermissionDenied as e:
        messages.warning(request , str(e))
    
    except InvalidForm as e:
        messages.error(request , str(e))
    
    except InvalidPassword as e:
        messages.error(request , str(e))
    return redirect(HTTP_REFERER)

@require_POST
@login_required(login_url = "login")
def del_image(request , id):
    user = request.user
    HTTP_REFERER = is_safe_url(request.META.get("HTTP_REFERER" , "/") , request.get_host())
    try:
        app_image_service.del_image(id , user)
        messages.success(request , "Successfully deleted image")
    except ObjectNotFound as e:
        messages.error(request , str(e))
    except PermissionDenied as e:
        messages.warning(request , str(e))
    except Exception as e:
        messages.info(request , "Something went wrong while deleting this image. Try again later")
    return redirect(HTTP_REFERER)


@require_POST
@login_required(login_url = "login")
def add_review(request , id):
    rating = request.POST.get("rating" , None)
    try:
        review = request.POST.get("review")
        review_service.add_review(app_id = id , user = request.user , review = review , rating = rating)
        messages.success(request , "Thanks for your review!")
    except AlreadyExists as e:
        messages.info(request , str(e))
    except PermissionDenied as e:
        messages.error(request , str(e))
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
    except ObjectNotFound as e:
        messages.error(request , str(e))
    return redirect(HTTP_REFERER)    

