from .models import Job , JobCategory
from django.db.models import Count , Q
from apps.exceptions import ObjectNotFound

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
    