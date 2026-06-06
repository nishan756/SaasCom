from .repository import JobRepo , JobCatRepo ,  ApplicationRepo
from saas_com.core.exceptions import PermissionDenied
from django.core.paginator import Paginator

class JobService:
    repo = JobRepo()

    def all_jobs(self , page_num , **query_set):
        supported_q_field = ["category" , "job_type" , "experience" , "title"]
        query_set = {key:value for key , value in query_set.items() if key in supported_q_field}
        jobs = self.repo.all_jobs(**query_set)
        paginator = Paginator(jobs , 15)
        jobs = paginator.get_page(page_num)
        return jobs
    
    def get_user_jobs(self , user):
        return self.repo.get_user_jobs(user)
    
    def job_detail(self , id):
        return self.repo.job_detail(id = id)
    
    def get_job(self , id):
        return self.repo.get_job(id = id)
    
    def post_job(self , user , form):
       job = form.save(commit = False)
       job.user = user
       self.repo.post_job(job)
        

class JobCatService:
    repo = JobCatRepo()

    def categories(self):
        return self.repo.categories()

class ApplicationService:
    repo = ApplicationRepo()

    def has_application(self , job_id , user):
        return self.repo.has_application(job_id , user)
    
    def get_application(self , id , user):
        return self.repo.get_application(id , user)

    def apply(self , user , form , job_id):
        job = JobService().job_detail(id = job_id)
        application = form.save(commit = False)
        application.job = job
        application.user = user
        return self.repo.apply(application)
    
    def total_applicants(self , job):
        return self.repo.total_applicants(job)
    
    def applications(self , id , user , page_num , **query_set):
        job = JobRepo().get_job(id)
        if job.user != user:
            raise PermissionDenied("You can\'t see applicants for this job")
        # Quering
        supported_q_fields = ["username" ,  "status"]
        query_set = {key:value for key , value in query_set.items() if key in supported_q_fields}
        
        # Pagination
        jobs = self.repo.applications(job = job , **query_set)
        paginator = Paginator(jobs , 20)
        jobs = paginator.get_page(page_num)
        return jobs
    
    def update_application_status(self , id , user , status , hr_message = None):
        application = self.get_application(id , user)
        if application.status != status:
            return self.repo.update_application_status(application , status , hr_message)
        
            