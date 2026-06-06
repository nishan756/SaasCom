from django.shortcuts import render , redirect
from django.core.exceptions import BadRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST , require_GET
from apps.views import is_safe_url

# ==============SERVICES=============
from .service import DiscussionService
from vote.service import VoteService
from report.service import ReportService
from comment.service import CommentService

# =============EXCEPTIONS============
from saas_com.core.exceptions import ObjectNotFound , InvalidForm

# ============FORMS==================
from .forms import DiscussionForm
from report.forms import ReportForm
from comment.forms import CommentForm

discussion_service = DiscussionService()
vote_service = VoteService()
report_service = ReportService()
comment_service = CommentService()


@require_GET
def all_discussions(request):
    page = request.GET.get("page" , 1)
    query_set = request.GET.dict()
    context = {}
    
    try:
        context["discussions"] = discussion_service.all_discussions(user = request.user , page = page , **query_set)
    except BadRequest as e:
        messages.info(request , str(e))

    return render(request , "discussions.html" , context)

@require_GET
def discussion_detail(request , id):
    try:
        discussion = discussion_service.discussion_detail(id)
    except ObjectNotFound as e:
        messages.error(request , str(e))
        return redirect("all-discussions")
    context = {}
    context["discussion"] = discussion
    context["report_form"] = ReportForm()
    context["comment_form"] = CommentForm()
    context["comments"] = comment_service.get_comments('discussion' , id)
    if request.user.is_authenticated:
        context["user_vote"] = vote_service.get_vote(user = request.user , content_type = "discussion" , object_id = id)
        context["user_report"] = report_service.has_user_report(content_type = "discussion" , object_id = id , reporter = request.user)

    return render(request , "discussion-detail.html" , context)

@login_required(login_url="login")
def post_discussion(request):

    if request.method == "POST":
        form = DiscussionForm(data = request.POST , files = request.FILES)

        try:
            discussion = discussion_service.post_discussion(request.user , form)
            messages.success(request , "Successfully posted your discussion")
            return redirect("discussion-detail" , id = discussion.id)
        except InvalidForm as e:
            messages.error(request , str(e))
        except Exception as e:
            messages.error(request , "Something went wrong")
    context = {}
    context["form"] = DiscussionForm()
    return render(request, "create-discussion.html", context)
    

@login_required(login_url = "login")
@require_POST
def delete_discussion(request , id):
    HTTP_REFERER = is_safe_url(url = request.META.get('HTTP_REFERER' , "/") , allowed_hosts = request.get_host())
    try:
        discussion_service.delete_discussion(user = request.user , id = id)
        messages.success(request , "Successfully deleted your discussion")
        return redirect("all-discussions")
    
    except ObjectNotFound as e:
        messages.error(request , str(e))
    
    except Exception as e:
        messages.error(request , "Something went wrong")

    return redirect(HTTP_REFERER)


@login_required(login_url = "login")
def update_discussion(request , id):
    try:
        discussion = discussion_service.get_discussion(user = request.user , id = id)

    except ObjectNotFound as e:
        messages.error(request , str(e))
        return redirect("all-discussions")
    
    context = {}
    context["form"] = DiscussionForm(instance = discussion)

    if request.method == "POST":
        form = DiscussionForm(data = request.POST , files = request.FILES , instance = discussion)

        try:
            discussion_service.update_discussion(form = form)
            messages.success(request , "Successfully updated your discussion")
            return redirect("discussion-detail" , id = id)
        
        except ObjectNotFound as e:
            messages.error(request , str(e))
        
        except Exception as e:
            messages.error(request , "Something went wrong")
            print(e)

        return redirect("all-discussions")
    return render(request , "create-discussion.html" , context)