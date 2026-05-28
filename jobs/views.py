from django.shortcuts import render , redirect
from django.views.decorators.http import require_GET , require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# =============Forms===============
from .forms import JobForm , ApplicationForm
from report.forms import ReportForm

# ============Service==============
from .service import JobService , JobCatService , ApplicationService
from session.service import BookmarkService
from report.service import ReportService

# ===========Exceptions============
from saas_com.core.exceptions import InvalidForm , ObjectNotFound , PermissionDenied


job_service = JobService()
application_service = ApplicationService()
job_cat_service = JobCatService()
bookmark_service = BookmarkService()
report_service = ReportService()



@require_GET
def all_jobs(request):
    # Query
    query_set = request.GET.dict()
    page_num = request.GET.get("page" , 1)
    jobs = job_service.all_jobs(page_num = page_num , **query_set)
    categories = job_cat_service.categories()
    context = {
        "jobs":jobs,
        "categories":categories
    }
    return render(request , "jobs.html" , context)

@require_GET
def job_detail(request , id):
    try:
        job = job_service.job_detail(id = id)
    except ObjectNotFound as e:
        messages.error(request , "The job you looking for doesn\'t found")
        return redirect("all-jobs")

    context = {}
    context["job"] = job
    context["job_form"] = JobForm()
    context["report_form"] = ReportForm()
    context["application_form"] = ApplicationForm()
    context["bookmark"] = bookmark_service.is_bookmarked(user= request.user ,content_type = "job", object_id = id) if request.user.is_authenticated else None
    context["application"] = application_service.has_application(job_id = id , candidate = request.user) if request.user.is_authenticated else None
    context["total_applicants"] = application_service.total_applicants(job)
    context["reports"] = report_service.get_reports(content_type = "job" , object_id = id)
    
    return render(request , "job-detail.html" , context)

@login_required(login_url = "login" , redirect_field_name = "post-job")
def post_job(request):
    if not request.user.is_company:
        messages.info(request , "You must have a company account to post job circular")
        return redirect("home") 
    
    form = JobForm()
    context = {}
    context["form"] = form
    if request.method == "POST" and request.user.is_company:
        form = JobForm(data = request.POST)
        if not form.is_valid():
            return messages.error(request , "Invalid Form data")
        try:
            job = job_service.post_job(company = request.user , form = form)
            messages.success(request , "Successfully posted your job")
            return redirect("job-detail" , id = job.id)
        
        except InvalidForm as e:
            messages.error(request , str(e))
        
        except PermissionError as e:
            messages.info(request , str(e))
            return redirect("home")
    return render(request , "post-job.html" , context)


@login_required(login_url = "login")
@require_POST
def apply(request , id):
    if request.method == "POST":
        form = ApplicationForm(data = request.POST , files = request.FILES)
    
    try:
        application_service.apply(candidate = request.user , form = form , job_id = id)
        messages.success(request , "Application successful")
    except ObjectNotFound as e:
        messages.error(request , str(e))
        return redirect("all-jobs")
    except Exception as e:
        messages.error(request , "Something went wrong")
    return redirect("job-detail" , id = id)

@login_required(login_url = "login")
@require_GET
def applications(request , id):
    context = {}
    query_set = request.GET.dict()
    page_num = request.GET.get("page" , 1)
    try:
        applications = application_service.applications(id = id , company = request.user , page_num = page_num , **query_set)
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
    return render(request , 'applications.html' , context)

@login_required(login_url = "login")
@require_GET
def application_detail(request , id):
    context = {}
    try:
        application = application_service.get_application(id , company = request.user)
    except ObjectNotFound as e:
        messages.error(request , str(e))
    context['application'] = application

    return render(request , "application-detail.html" , context)


@login_required(login_url = "login")
@require_POST
def update_application_status(request , id , status):
    if not request.user.is_company:return redirect("home")
    job_id = request.POST.get("job_id")
    hr_message = request.POST.get("hr_message" , None)
    try:
        application_service.update_application_status(id = id , company = request.user , status = status , hr_message = hr_message)
        messages.success(request , "Successfully updated application status")
        return redirect("application-detail" , id)
    
    except ObjectNotFound as e:
        messages.error(request , str(e))
        return redirect()
    
    except Exception as e:
        messages.error(request , "Something went wrong")
    
    return redirect("applications" , job_id)