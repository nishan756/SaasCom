from django.shortcuts import render , redirect
from django.core.exceptions import BadRequest
from django.contrib import messages

# ==============SERVICES=============
from .service import DiscussionService
from vote.service import VoteService

# =============EXCEPTIONS============
from saas_com.core.exceptions import ObjectNotFound


discussion_service = DiscussionService()
vote_service = VoteService()

def all_discussions(request):
    page = request.GET.get("page" , 1)
    query_set = request.GET.dict()
    context = {}
    
    try:
        context["discussions"] = discussion_service.all_discussions(user = request.user , page = page , **query_set)
    except BadRequest as e:
        messages.info(request , str(e))

    return render(request , "discussions.html" , context)

def discussion_detail(request , id):
    try:
        discussion = discussion_service.discussion_detail(id)
    except ObjectNotFound as e:
        messages.error(request , str(e))
        return redirect("all-discussions")
    context = {}
    context["discussion"] = discussion
    context["has_vote"] = vote_service.get_vote(user = request.user , content_type = "discussion" , object_id = id) if request.user.is_authenticated else None

    return render(request , "discussion-detail.html" , context)


def create_discussion(request):pass

def delete_discussion(request):pass