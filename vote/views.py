from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from apps.views import is_safe_url

from .service import VoteService

from saas_com.core.exceptions import ObjectNotFound , PermissionDenied


vote_service = VoteService()

@require_POST
@login_required(login_url = "login")
def vote(request , content_type_str , id):
    HTTP_REFERER = is_safe_url(request.META.get("HTTP_REFERER") , request.get_host())
    vote_type = request.POST.get("vote_type")
    try:
        msg = vote_service.vote(user = request.user , content_type_str = content_type_str , object_id = id , vote_type = vote_type)
        messages.success(request , msg)

    except ObjectNotFound as e:
        messages.error(request , "App not found")
        return redirect("all-apps")

    except PermissionDenied as e:
        messages.info(request , str(e))
        return redirect(HTTP_REFERER)
    
    except Exception as e:
        messages.error(request , "Somethig went wrong")
    
    return redirect(HTTP_REFERER)

