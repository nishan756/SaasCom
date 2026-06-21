from .repository import JobRepo , JobCatRepo ,  ApplicationRepo
from saas_com.core.exceptions import PermissionDenied , AlreadyExists , InvalidForm
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
    
    def get_user_jobs(self , user , page , **query_param):
        supported_query_field = ["date_from" , "date_to" , "is_active" , "deadline"]
        query_param = {key:value for key , value in query_param.items() if key in supported_query_field}
        jobs = self.repo.get_user_jobs(user , **query_param)
        paginator = Paginator(jobs , 20)
        jobs = paginator.get_page(page)
        return jobs
    
    def job_detail(self , id):
        return self.repo.job_detail(id = id)
    
    def get_job(self , id):
        return self.repo.get_job(id = id)
    
    def post_job(self , user , form):
        job_credentials = form.cleaned_data.copy()
        skills = job_credentials.pop("skills" , [])
        job_credentials["user"] = user

        return self.repo.post_job(skills , **job_credentials)
    
    def update_job(self , form):
       job = form.save(commit = False)
       skills = form.cleaned_data.get("skills")
       return self.repo.update_job(job , skills)
    
    def delete_job(self , user , job):
        if job.user != user:
            raise PermissionDenied("OOPS! Can't perform this operation")
        
        return self.repo.delete_job(job)
        

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
    
    def get_user_applications(self , user , page_num , **query_param):
        valied_query_fields = ["job_title" , "status" , "company" , "applied_at"]
        query_param = {field:value for field , value in query_param.items() if field in valied_query_fields}
        applications =  self.repo.get_user_applications(user , **query_param)
        # Paginating
        paginator = Paginator(applications , 15)
        applications = paginator.get_page(page_num)
        return applications

    def apply(self , user , form , job_id):

        job = JobService().job_detail(id = job_id)

        if job.user == user:
            raise PermissionDenied("Recruiter can't apply their job")

        elif self.has_application(job_id = job_id , user = user):
            raise AlreadyExists("You already applied in this job")
        
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
        
        if application.hr_message:
            application.hr_message = None

        if application.status != status:
            if application.hr_message:
                application.hr_message = None
            return self.repo.update_application_status(application , status , hr_message)
        
            