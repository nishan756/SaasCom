from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET , require_POST
from django.contrib import messages


# ===========SERVICES=============
from apps.service import AppService , ReviewService
from jobs.service import ApplicationService , JobService
from discussion.service import DiscussionService
from vote.service import VoteService

# ===========Exceptions===========
from saas_com.core.exceptions import ObjectNotFound , PermissionDenied


app_service = AppService()
application_service = ApplicationService()
job_service = JobService()
discussion_service = DiscussionService()
vote_service = VoteService()
review_service = ReviewService()


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
        context["avg_rating"] = review_service.get_app_rating_stats(context["app"] , **query_param)
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
    page_num = query_param.pop("page" , 1)
    if not request.user.is_developer:
        messages.info(request , "This feature isn't available for you")
        return redirect("home")
    context = {}
    context["applications"] = application_service.get_user_applications(request.user , page_num , **query_param)
    return render(request , "my-applications.html" , context)

@login_required(login_url = "login")
@require_GET
def jobs_dashboard(request):
    query_param = request.GET.dict()
    page = query_param.pop("page" , 1)
    context = {}
    context["jobs"] = job_service.get_user_jobs(request.user , page , **query_param)
    return render(request , "jobs-dashboard.html" , context)

@login_required(login_url = "login")
@require_GET
def job_applications(request , id):
    context = {}
    query_set = request.GET.dict()
    page_num = query_set.pop("page" , 1)
    try:
        applications = application_service.applications(id = id , user = request.user , page_num = page_num , **query_set)
    except ObjectNotFound as e:
        messages.error(request , str(e))
        return redirect("profile" , request.user.username)
    except PermissionDenied as e:
        messages.warning(request , str(e))
        return redirect("profile" , request.user.username)
    except Exception as e:
        messages.info(request , "Something went wrong")
        return redirect("profile" , request.user.username)
    context['applications'] = applications
    return render(request , 'job-applications.html' , context)


@login_required(login_url = "login")
@require_POST
def update_application_status(request , id , status):
    if not request.user.is_company:
        return redirect("home")
    job_id = request.POST.get("job_id")
    hr_message = request.POST.get("hr_message" , None)
    try:
        application_service.update_application_status(id = id , user = request.user , status = status , hr_message = hr_message)
        messages.success(request , "Successfully updated application status")
        return redirect("application-detail" , id)
    
    except ObjectNotFound as e:
        messages.error(request , str(e))
        return redirect()
    
    except Exception as e:
        messages.error(request , "Something went wrong")
    
    return redirect("applications" , job_id)


@login_required(login_url = "login")
@require_GET
def application_detail(request , id):
    context = {}
    try:
        application = application_service.get_application(id , user = request.user)
    except ObjectNotFound as e:
        messages.error(request , str(e))
    context['application'] = application

    return render(request , "application-detail.html" , context)

@login_required(login_url = "login")
@require_GET
def job_stats(request):
    query_param = request.GET.dict()
    context = {}
    return render(request , "job-stats.html" , context)


@login_required(login_url = "login")
@require_GET
def discussion_dashboard(request):
    context = {}
    return render(request , "discussion-dashboard.html" , context)

