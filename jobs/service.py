from .repository import JobRepo , JobCatRepo
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