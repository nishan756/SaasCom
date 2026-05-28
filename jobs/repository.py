from .models import Job , JobCategory , Application
from django.db.models import Count , Q
from saas_com.core.exceptions import ObjectNotFound

class JobRepo:

    def all_jobs(self , **query_set):
        jobs = Job.objects.select_related("company" , "category")
        if query_set.get("category"):
            jobs = jobs.category(category = query_set["category"])
        if query_set.get("job_type"):
            jobs = jobs.job_type(query_set["job_type"])
        if query_set.get("experience"):
            jobs = jobs.experience(query_set["experience"])
        if query_set.get("title"):
            jobs = jobs.filter(title__icontains = query_set["title"])
        return jobs
    
    def get_company_jobs(self , company):
        return Job.objects.filter(company = company)
    
    def get_job(self , id):
        try:
            return Job.objects.select_related("company").get(id = id)
        except Job.DoesNotExist:
            raise ObjectNotFound("Job post not found")
    
    def job_detail(self , id):
        try:
            return Job.objects.select_related("company" , "category").get(id = id)
        except Job.DoesNotExist:
            raise ObjectNotFound("Job post not found")

    def post_job(self , job):
        return job.save()

class JobCatRepo:

    def categories(self):
        return JobCategory.objects.prefetch_related("jobs").annotate(
            active_jobs = Count("jobs" , filter = Q(jobs__is_active = True)),
        )


class ApplicationRepo:

    def has_application(self , job_id , candidate):
        return Application.objects.filter(Q(job__id = job_id) , Q(candidate = candidate)).exists()
    
    def get_application(self , id , company):
        try:
            return Application.objects.select_related("candidate").get(id = id , job__company = company)
        except Application.DoesNotExist:
            raise ObjectNotFound("Application not found")

    def apply(self , application):
        return application.save()
    
    def total_applicants(self , job):
        return Application.objects.filter(job = job).count()
    
    def applications(self , job , **query_set):
        applications = Application.objects.select_related("candidate").filter(job = job)
        if query_set.get("username"):
            applications = applications.filter(candidate__username = query_set["username"])
        if query_set.get("status"):
            applications = applications.filter(status = query_set["status"])
        return applications
    
    def update_application_status(self , application , status , hr_message = None):
        application.status = status
        if hr_message:application.hr_messages = hr_message
        return application.save() 

         
    
