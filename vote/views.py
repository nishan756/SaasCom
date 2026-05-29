from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from .service import VoteService

from saas_com.core.exceptions import ObjectNotFound , InvalidContentType


vote_service = VoteService()

@require_POST
@login_required(login_url = "login")
def vote(request , content_type , id):
    vote_type = request.POST.get("vote_type")
    try:
        msg = vote_service.vote(user = request.user , content_type = content_type , object_id = id , vote_type = vote_type)
        messages.success(request , msg)

    except ObjectNotFound as e:
        messages.error(request , "App not found")
        return redirect("all-apps")
    
    except Exception as e:
        messages.error(request , "Somethig went wrong")
        print(e) 
    
    return redirect("app-detail" , id)

