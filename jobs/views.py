from django.shortcuts import render , redirect
from django.views.decorators.http import require_GET , require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from saas_com.core.service import is_safe_url

# =============Forms===============
from .forms import JobForm , ApplicationForm
from report.forms import ReportForm

# ============Service==============
from .service import JobService , JobCatService , ApplicationService
from bookmark.service import BookmarkService
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
    page_num = query_set.pop("page" , 1)
    categories = job_cat_service.categories()
    try:
        jobs = job_service.all_jobs(page_num = page_num , **query_set)

    except InvalidForm as e:
        messages.error(request , str(e))
        return redirect("home")
    
    except Exception as e:
        messages.error(request , "Something went wrong")
        return redirect("home")
    
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
    context["application"] = application_service.has_application(job_id = id , user = request.user) if request.user.is_authenticated else None
    context["total_applicants"] = application_service.total_applicants(job)
    context["user_report"] = report_service.has_user_report('job' , id , request.user) if request.user.is_authenticated else None
    context["reports"] = report_service.get_reports(content_type_str = "job" , object_id = id)
    
    return render(request , "job-detail.html" , context)

@login_required(login_url="login", redirect_field_name="post-job")
def post_job(request):
    if not request.user.is_company:
        messages.info(request, "You must have a company account to post job circular")
        return redirect("all-jobs") 
    
    if request.method == "POST":
        form = JobForm(data=request.POST)
        
        if form.is_valid():
            try:
                job = job_service.post_job(user=request.user, form=form)
                messages.success(request, "Successfully posted your job")
                return redirect("job-detail", id=job.id)
            except Exception as e:
                messages.error(request, f"Something went wrong: {str(e)}")
        else:
            messages.error(request, form.errors)
            
    else:
        form = JobForm()

    context = {
        "form": form,
        "instance": False
    }
    return render(request, "post-job.html", context)

@login_required(login_url = "login")
def update_job(request , id):
    HTTP_REFERER = is_safe_url(request.META.get("HTTP_REFERER") , request.get_host())
    
    # Fetching the job object
    job = job_service.get_job(id)

    # Checking if the user is recruiter
    if request.user != job.user:
        messages.info(request , "You can't update this job post")
        return redirect("all-jobs")
    
    if request.method == "POST":
        try:
        
            form = JobForm(data = request.POST , files = request.FILES , instance = job)
            job_service.update_job(form)
            messages.success(request , "Successfully updated your job post")
            return redirect("job-detail" , id)

        except ObjectNotFound as e:
            messages.error(request , str(e))
            return redirect("all-jobs")
        
        except Exception as e:
            messages.info(request , "Something went wrong. Try again later")
        
        return redirect(HTTP_REFERER)

    context = {}
    context["form"] = JobForm(instance = job)
    context["instance"] = True
    return render(request , "post-job.html" , context)

@login_required(login_url = "login")
@require_POST
def delete_job(request , id):
    HTTP_REFERER = is_safe_url(request.META.get("HTTP_REFERER" , "/") , request.get_host())
    try:
        job = job_service.get_job(id)
        job_service.delete_job(request.user, job)
    
    except ObjectNotFound as e:
        messages.error(request , str(e))
    
    except PermissionDenied as e:
        messages.warning(request , str(e))
    
    except Exception as e:
        messages.error(request , "Something went wrong")
    
    return redirect(HTTP_REFERER)

@login_required(login_url = "login")
@require_POST
def apply(request , id):
    form = ApplicationForm(data = request.POST , files = request.FILES)
    
    try:
        application_service.apply(user = request.user , form = form , job_id = id)
        messages.success(request , "Application successful")
    except ObjectNotFound as e:
        messages.error(request , str(e))
        return redirect("all-jobs")
    except Exception as e:
        messages.error(request , "Something went wrong")
    return redirect("job-detail" , id = id)


