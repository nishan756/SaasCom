from .models import Job
from apps.exceptions import ObjectNotFound

class JobRepo:
    queryset = Job.objects.all()

    def all_jobs(self):
        jobs = self.queryset.select_related("company" , "category").active_jobs()
        return jobs
    
    def job_detail(self , id):
        try:
            return self.queryset.select_related("company" , "category").get(id = id)
        except Job.DoesNotExist:
            raise ObjectNotFound("Job post not found")

    def post_job(self , job):
        return job.save()
