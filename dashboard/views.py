from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET , require_POST
from django.contrib import messages
from jobs.models import Application , JobCategory , Job
from apps.models import App
from urllib.parse import urlencode


# ===========SERVICES=============
from apps.service import AppService , ReviewService
from jobs.service import ApplicationService , JobService
from discussion.service import DiscussionService
from vote.service import VoteService
from .service import DiscussionDashboardService, JobDashboardService , ApplicationDashboardService , AppsDashboardService

# ===========Exceptions===========
from saas_com.core.exceptions import ObjectNotFound , PermissionDenied , InvalidForm

job_dashboard_service = JobDashboardService()
app_service = AppService()
application_service = ApplicationService()
job_service = JobService()
discussion_service = DiscussionService()
vote_service = VoteService()
review_service = ReviewService()
discussion_dashboard_service = DiscussionDashboardService()
application_dashboard_service = ApplicationDashboardService()
apps_dashboard_service = AppsDashboardService()


@login_required(login_url = "login")
@require_GET
def dashboard_entry_point(request):
    return render(request , "dashboard-entry-point.html")


@login_required(login_url = "login")
@require_GET
def apps_dashboard(request):
    query_param = request.GET.dict()

    page = query_param.pop("page" , 1)

    try:
        result = apps_dashboard_service.main_dashboard(request.user , page , **query_param)
    
    except Exception as e:
        messages.error(request , "Something went wrong")
        return redirect("apps-dashboard")

    context = {
            "apps":result.pop("apps"),
            "top_apps":result.pop("top_apps"),
            "stats":result.pop("stats"),
            "statuses":App.get_app_status_as_dict(),
            "query_param":urlencode(query_param)
        }

    return render(request , "apps-dashboard.html" , context )


@login_required(login_url = "login")
@require_GET
def app_stats(request , id):
    query_param = request.GET.dict()
    context = {}
    try:
        result = apps_dashboard_service.app_stats(request.user , id , **query_param)
        
        context["app"] = result.pop("app")
        context["stats"] = result.pop("stats")

        return render(request , "app-stats.html" , context)

    except ObjectNotFound as e:
        messages.info(request , str(e))

    except Exception as e:
        messages.info(request , "Something went wrong")

    return redirect("apps-dashboard")

@login_required(login_url = "login")
@require_GET
def user_application_dashboard(request):
    query_param = request.GET.dict()
    page_num = query_param.pop("page" , 1)

    per_page = query_param.pop("per_page" , 20)

    if not request.user.is_developer:
        messages.info(request , "This feature isn't available for you")
        return redirect("dashboard-entry-point")
    
    context = {}

    try:
        result = application_dashboard_service.main_dashboard(request.user , per_page , page_num , **query_param)
        context["categories"] = JobCategory.objects.select_related("parent").all()
        context["job_types"] = Job().get_job_type_as_dict()
        context.update(result)
        context["statuses"] = Application.get_application_status_dict()
        return render(request , "user-application-dashboard.html" , context)
    
    except Exception as e:
        messages.error(request , "Somethinf went wrong")

    return redirect("dashboard-entry-point")

@login_required(login_url = "login")
@require_GET
def jobs_dashboard(request):
    # Checking if the user is company
    if not request.user.is_company:
        messages.info(request , "This feature isn't available for you")
        return redirect("dashboard-entry-point")
    
    query_param = request.GET.dict()
    page = query_param.pop("page" , 1)
    per_page = query_param.pop("per_page" , 20)
    context = {}

    try:
        result = job_dashboard_service.main_dashboard(request.user , page , per_page , **query_param)
        context["jobs"] = result["jobs"]
        context["stats"] = result["stats"]
        context["query_param"] = urlencode(query_param)
        return render(request , "jobs-dashboard.html" , context)
    
    except Exception as e:
        messages.error(request , "Something went wrong")

    return redirect("dashboard-entry-point")

@login_required(login_url = "login")
@require_GET
def job_applications(request , id):
    context = {}
    query_set = request.GET.dict()
    page_num = query_set.pop("page" , 1)
    try:
        applications = application_service.applications(id = id , user = request.user , page_num = page_num , **query_set)
        context['applications'] = applications
        context["statuses"] = Application().get_application_status_dict()
        return render(request , 'job-applications.html' , context)
    except ObjectNotFound as e:

        messages.error(request , str(e))
    
    except PermissionDenied as e:
        messages.warning(request , str(e))
    
    except Exception as e:
        messages.info(request , "Something went wrong")
        
    return redirect("job-applications" , id)


@login_required(login_url = "login")
@require_POST
def update_application_status(request , id , status):
    
    job_id = request.POST.get("job_id" , None)
    try:
        application_service.update_application_status(
            id=id,
            user=request.user,
            status=status,
        )
        messages.success(request, "Successfully updated application status")
        return redirect("application-detail" , id)

    except ObjectNotFound as e:
        messages.error(request, str(e))

    except InvalidForm as e:
        messages.info(request, str(e))
    
    except PermissionDenied as e:
        messages.warning(request , str(e))

    return redirect("job-applications" , job_id if request.user.is_company else "user-application-dashboard")


@login_required(login_url="login")
@require_GET
def application_detail(request, id):
    try:
        application = application_service.get_application(id)
    except ObjectNotFound as exc:
        messages.error(request, str(exc))
        return redirect(
            "job-applications"
            if request.user.is_company
            else "user-application-dashboard"
        )

    is_applicant = application.user == request.user
    is_company = application.job.user == request.user

    if not (is_applicant or is_company):
        messages.warning(request, "You can't view this application")
        return redirect(
            "job-applications"
            if request.user.is_company
            else "user-application-dashboard"
        )

    context = {
        "application": application,
        "actions": ApplicationService.application_actions()
            .get(request.user.user_type, {})
            .get(application.status, {}),
    }

    return render(request, "application-detail.html", context)

@login_required(login_url = "login")
@require_GET
def job_stats(request , id):

    try:
        result = job_dashboard_service.job_stats(id)
        return render(request , "job-stats.html" , result)

    except ObjectNotFound as e:
        messages.error(request , str(e))
    
    return redirect("jobs-dashboard")


@login_required(login_url = "login")
@require_GET
def discussion_dashboard(request):
    query_param = request.GET.dict()
    context = {}
    try:
        result = discussion_dashboard_service.main_dashboard(request.user , **query_param)
        context["stats"] = result["stats"]
        context["discussions"] = result["discussions"]
    
    except Exception as e:
        messages.info(request , "This page has some issues.")
        return redirect('dashboard-entry-point')
    
    return render(request , "discussion-dashboard.html" , context)


@login_required(login_url = "login")
@require_GET
def discussion_stats(request , id):
    query_param = request.GET.dict()
    context = {}
    try:
        context["discussion"] = discussion_service.get_discussion(request.user , id)
        result = discussion_dashboard_service.discussion_stats(id , **query_param)

        context["comments"] = result.get("comments")
        context["reports"] = result.get("reports")

        context["stats"] = result.get("stats")

        return render(request , "discussion-stats.html" , context)
    
    except ObjectNotFound as e:
        messages.error(request , str(e))
    
    except Exception as e:
        messages.error(request , "Something went wrong")

    return redirect("discussion-dashboard")
