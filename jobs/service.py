from .repository import JobRepo
from session.exceptions import InvalidForm
from django.core.paginator import Paginator

class JobService:
    repo = JobRepo()

    def all_jobs(self , page_num):
        apps = self.repo.all_jobs()
        paginator = Paginator(apps , per_page = 15)
        page_num = page_num
        apps = paginator.get_page(number = page_num)
        return self.repo.all_jobs()
    
    def job_detail(self , id):
        return self.repo.job_detail(id = id)
    
    def post_job(self , company , form):
       
        if form.is_valid():
            job = form.save(commit = False)
            job.company = company
            return self.repo.post_job(job)
        raise InvalidForm(form.errors.as_text())
    