from django.shortcuts import render , redirect
from django.views.decorators.http import require_GET , require_POST
from django.contrib.auth.decorators import login_required
from apps.views import is_safe_url
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from .models import Job

# =============Forms===============
from .forms import JobForm , ApplicationForm
from session.forms import ReportForm

# ============Service==============
from .service import JobService , JobCatService , ApplicationService
from session.service import BookmarkService

# ===========Exceptions============
from session.exceptions import InvalidForm
from apps.exceptions import ObjectNotFound


job_service = JobService()
application_service = ApplicationService()
job_cat_service = JobCatService()
bookmark_service = BookmarkService()



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
    job_form = JobForm()
    report_form = ReportForm()
    application_form = ApplicationForm()
    bookmark = bookmark_service.is_bookmarked(user= request.user ,content_type = "job", object_id = id) if request.user.is_authenticated else None
    application = application_service.has_application(job_id = id , candidate = request.user) if request.user.is_authenticated else None
    try:
        job = job_service.job_detail(id = id)
    except ObjectNotFound as e:
        messages.error(request , "The job you looking for doesn\'t found")
        return redirect("all-jobs")
    return render(request , "job-detail.html" , context = {"job":job , "job_form":job_form , "report_form":report_form , "application_form":application_form , "bookmark":bookmark , "application":application})

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
