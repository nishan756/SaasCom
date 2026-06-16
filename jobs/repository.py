from .models import Job , JobCategory , Application
from django.db.models import Count , Q
from saas_com.core.exceptions import ObjectNotFound

class JobRepo:

    def all_jobs(self , **query_set):
        jobs = Job.objects.select_related("user" , "category" , "currency")
        if query_set.get("category"):
            jobs = jobs.category(category = query_set["category"])
        if query_set.get("job_type"):
            jobs = jobs.job_type(query_set["job_type"])
        if query_set.get("experience"):
            jobs = jobs.experience(query_set["experience"])
        if query_set.get("title"):
            jobs = jobs.filter(title__icontains = query_set["title"])
        return jobs
    
    def get_user_jobs(self , user):
        return Job.objects.filter(user = user)
    
    def get_job(self , id):
        try:
            return Job.objects.select_related("user").get(id = id)
        except Job.DoesNotExist:
            raise ObjectNotFound("Job post not found")
    
    def job_detail(self , id):
        try:
            return Job.objects.select_related("user" , "category").get(id = id)
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

    def has_application(self , job_id , user):
        return Application.objects.filter(Q(job__id = job_id) , Q(user = user)).exists()
    
    def get_application(self , id , user):
        try:
            return Application.objects.select_related("user").get(id = id , job__user = user)
        except Application.DoesNotExist:
            raise ObjectNotFound("Application not found")
    
    def get_user_applications(self , user , **query_param):
        applications = Application.objects.only("status" , "applied_at" , "job__title" , "job__user").select_related("job" , "job__user").filter(user = user)

        if query_param.get("job_title"):
            applications = applications.filter(job__title__icontains = query_param["job_title"])
        
        if query_param.get("status"):
            applications = applications.filter(status = query_param["status"])
        
        if query_param.get("applied_at"):
            applications = applications.filter(applied_at__date = query_param["applied_at"])

        return applications

    def apply(self , application):
        return application.save()
    
    def total_applicants(self , job):
        return Application.objects.filter(job = job).count()
    
    def applications(self , job , **query_set):
        applications = Application.objects.select_related("user").filter(job = job)
        if query_set.get("username"):
            applications = applications.filter(user__username = query_set["username"])
        if query_set.get("status"):
            applications = applications.filter(status = query_set["status"])
        return applications
    
    def update_application_status(self , application , status , hr_message = None):
        application.status = status
        if hr_message:application.hr_message = hr_message
        return application.save() 

         
    
