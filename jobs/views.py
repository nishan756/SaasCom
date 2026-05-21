from django.shortcuts import render , redirect
from django.views.decorators.http import require_GET , require_POST
from django.contrib.auth.decorators import login_required
from apps.views import is_safe_url
from django.contrib import messages

# =============Forms===============
from .forms import JobForm , ApplicationForm
from session.forms import ReportForm

# ============Service==============
from .service import JobService

# ===========Exceptions============
from session.exceptions import InvalidForm
from apps.exceptions import ObjectNotFound


job_service = JobService()



@require_GET
def all_jobs(request):
    page_num = request.GET.get("page_num")
    jobs = job_service.all_jobs(page_num = page_num)
    context = {
        "jobs":jobs
    }
    return render(request , "jobs.html" , context)

@require_GET
def job_detail(request , id):
    job_form = JobForm()
    report_form = ReportForm()
    application_form = ApplicationForm()
    try:
        job = job_service.job_detail(id = id)
    except ObjectNotFound as e:
        messages.error(request , "The job you looking for doesn\'t found")
        return redirect("all-jobs")
    return render(request , "job-detail.html" , context = {"job":job , "job_form":job_form , "report_form":report_form , "application_form":application_form})

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


