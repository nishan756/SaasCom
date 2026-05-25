from .repository import JobRepo , JobCatRepo ,  ApplicationRepo
from session.exceptions import InvalidForm
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
    
    def job_detail(self , id):
        return self.repo.job_detail(id = id)
    
    def post_job(self , company , form):
       job = form.save(commit = False)
       job.company = company
       self.repo.post_job(job)
        

class JobCatService:
    repo = JobCatRepo()

    def categories(self):
        return self.repo.categories()

class ApplicationService:
    repo = ApplicationRepo()

    def has_application(self , job_id , candidate):
        return self.repo.has_application(job_id , candidate)

    def apply(self , candidate , form , job_id):
        job = JobService().job_detail(id = job_id)
        application = form.save(commit = False)
        application.job = job
        application.candidate = candidate
        return self.repo.apply(application)
    
    def total_applicants(self , job):
        return self.repo.total_applicants(job)