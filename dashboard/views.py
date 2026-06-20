from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.contrib import messages


# ===========SERVICES=============
from apps.service import AppService
from jobs.service import ApplicationService , JobService
from discussion.service import DiscussionService
from vote.service import VoteService

# ===========Exceptions===========
from saas_com.core.exceptions import ObjectNotFound


app_service = AppService()
application_service = ApplicationService()
job_service = JobService()
discussion_service = DiscussionService()
vote_service = VoteService()


@login_required(login_url = "login")
@require_GET
def dashboard_entry_point(request):
    return render(request , "dashboard-entry-point.html")

@login_required(login_url = "login")
@require_GET
def apps_dashboard(request):
    context = {}
    user_apps = app_service.get_user_apps(request.user)
    context["apps"] = user_apps.get("apps")
    context['total_pending_apps'] = user_apps.get("total_pending_apps")
    context['total_rejected_apps'] = user_apps.get("total_rejected_apps")

    return render(request , "apps-dashboard.html" , context)

@login_required(login_url = "login")
@require_GET
def app_stats(request , id):
    query_param = request.GET.dict()
    context = {}
    try:
        context["app"] = app_service.get_app(id = id)

        if not context["app"].user == request.user:
            return redirect("apps-dashboard")
        
        vote_stats = vote_service.get_object_votes_stats('app' , id , **query_param)
        context["total_upvote"] = vote_stats["total_upvote"]
        context["total_downvote"] = vote_stats["total_downvote"]
        return render(request , "app-stats.html" , context)

    except ObjectNotFound as e:
        messages.info(request , str(e))

    except Exception as e:
        messages.error(request , "Something went wrong")
        
    return redirect("apps-dashboard")

@login_required(login_url = "login")
@require_GET
def my_applications(request):
    query_param = request.GET.dict()
    page_num = request.GET.get("page" , 1)
    if not request.user.is_developer:
        messages.info(request , "This feature isn't available for you")
        return redirect("home")
    context = {}
    context["applications"] = application_service.get_user_applications(request.user , page_num , **query_param)
    return render(request , "my-applications.html" , context)

@login_required(login_url = "login")
@require_GET
def jobs_dashboard(request):
    context = {}
    return render(request , "jobs-dashboard" , context)


@login_required(login_url = "login")
@require_GET
def discussion_dashboard(request):
    context = {}
    return render(request , "discussion-dashboard.html" , context)

