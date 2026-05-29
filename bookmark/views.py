from django.shortcuts import render , redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from apps.views import is_safe_url

# ==================Services=====================
from .service import BookmarkService

# ==================Exceptions=====================
from saas_com.core.exceptions import AlreadyExists , ObjectNotFound

bookmark_service = BookmarkService()

@login_required(login_url = "login")
@require_POST
def add_bookmark(request , object_id):
    HTTP_REFERER = is_safe_url(request.META.get("HTTP_REFERER") , allowed_hosts = request.get_host())
    content_type = request.POST.get("content_type")
    try:
        bookmark_service.add_bookmark(user = request.user , content_type = content_type , object_id = object_id)
        messages.success(request , f"This {content_type} is added to your bookmark")
    
    except AlreadyExists as e:
        messages.info(request , str(e))
    
    except Exception as e:
        messages.error(request , "Something went wrong")

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