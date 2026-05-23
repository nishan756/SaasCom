from django.shortcuts import render , redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from django.views.decorators.http import require_GET , require_POST
from django.contrib.auth.decorators import login_required

# ===================MODELS================
from .models import App
# ====================SERVICES=============
from .service import AppService , VoteService , AppImageService , ReviewService
from session.service import FollowService , UserService , ReportService

# ==================EXCEPTIONS=============
from .exceptions import AlreadyExists , ObjectNotFound, PermissionDenied , TooManyImage
from session.exceptions import InvalidForm , InvalidPassword

# =================FORMS=================
from .forms import ReviewForm , AppForm , AppDeletionConfirmationForm
from session.forms import ReportForm



# =========SERVICES=========
app_service = AppService()
vote_service = VoteService()
app_image_service = AppImageService()
review_service = ReviewService()
user_service = UserService()
follow_service = FollowService()
report_service = ReportService()

def is_safe_url(url , allowed_hosts):
    if url_has_allowed_host_and_scheme(url , allowed_hosts = allowed_hosts):
        return url
    return "/"

@require_GET
def home(request):
    total_apps = app_service.total_apps()
    total_users = user_service.total_user()
    content = {
        "total_apps": total_apps,
        "total_users": total_users
    }
    return render(request , "index.html" , content)


@require_GET
def all_apps(request):
    order_by = request.GET.get("order_by" , None)
    context = {}
    context["apps"] = app_service.all_apps(order_by = order_by)
    return render(request , "apps.html" , context)

@require_GET
def app_detail(request , id):
    context = {}
    try:
        context["app"] = app_service.get_app_detail(id = id)
    except ObjectNotFound as e:
        messages.info(request , str(e))
        return redirect("all-apps")
    context["user_vote"] = vote_service.has_vote(context["app"], request.user)
    context["form"] = ReviewForm()
    context["user_vote"] = vote_service.has_vote(context["app"], request.user) if request.user.is_authenticated else None
    context["is_following"] = follow_service.is_following(request.user, context["app"].founder) if request.user.is_authenticated else False
    context["app_del_form"] = AppDeletionConfirmationForm()
    context["report_form"] = ReportForm()
    context["user_report"] = report_service.has_user_report(content_type = "app" , object_id = id , reporter = request.user)
    return render(request , "app-detail.html" , context)

@login_required(login_url = "login")
def create_app(request):
    if request.method == "POST":
        form = AppForm(request.POST , request.FILES)
        try:
            new_app = app_service.create_app(founder = request.user , form = form)
            images = request.FILES.getlist("images")
            if images:
                app_image_service.add_images(app = new_app , images = images)
            return redirect("app-detail" , id = new_app.id)
        except InvalidForm as e:
            messages.error(request , str(e))
            return render(request , "create-app.html" , {"form":form})
        
        except TooManyImage as e:
            messages.info(request , str(e))
        
        except Exception as e:
            messages.info("Something went wrong. Please try again later")
    else:
        form = AppForm()
        return render(request , "create-app.html" , {"form":form})

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
    founder = request.user
    HTTP_REFERER = is_safe_url(request.META.get("HTTP_REFERER" , "/") , request.get_host())
    try:
        app_image_service.del_image(id , founder)
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
def vote(request , id):
    vote_type = request.POST.get("vote_type")
    try:
        msg = vote_service.vote(app_id = id , user = request.user , vote_type = vote_type)
        messages.success(request , msg)
    except ObjectNotFound as e:
        messages.error(request , message = e)
    return redirect("app-detail" , id)

@require_POST
@login_required(login_url = "login")
def add_review(request , id):
    try:
        review = request.POST.get("review")
        review_service.add_review(app_id = id , user = request.user , review = review)
        messages.success(request , "Thanks for your review!")
    except AlreadyExists as e:
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
    except ObjectNotFound as e:
        messages.error(request , str(e))
    return redirect(HTTP_REFERER)    

