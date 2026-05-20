from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django_summernote.fields import SummernoteTextField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

User = get_user_model()


class JobCategory(models.Model):
    title = models.CharField(max_length = 100 , unique = True)
    parent = models.ForeignKey("self" ,on_delete = models.CASCADE , blank = True , null = True , related_name = "sub_categories")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]

class JobQueryset(models.QuerySet):

    def job_type(self , job_type):
        return self.filter(job_type = job_type)
    
    def active_jobs(self):
        return self.filter(is_active = True)
    
    def salary(self , max_salary = None , min_salary = None):
        if max_salary is not None and min_salary is not None:
            return self.filter(min_salary__gte = min_salary , max_salary__lte = max_salary)
        
        elif min_salary is not None:
            return self.filter(min_salary__gte = min_salary) 
        
        elif max_salary is not None:
            return self.filter(max_salary__lte = max_salary)
        return self

    def category(self , category):
        return self.filter(category__title__iexact = category)
    
    def experience(self , experience):
        return self.filter(experience = self.experience)

class JobManager(models.Manager):
    
    def get_queryset(self):
        return JobQueryset(model = self.model , using = self._db)
    
    def job_type(self , job_type):
        return self.get_queryset().job_type(job_type = job_type)
    
    def active_jobs(self):
        return self.get_queryset().active_jobs()
    
    
    def salary(self , max_salary = None , min_salary = None):
        return self.get_queryset().salary(max_salary = max_salary , min_salary = min_salary)

    def category(self , category):
        return self.get_queryset().category(category = category) 
    
    def experience(self , experience):
        return self.get_queryset().experience(experience = self.experience)
    

class Job(models.Model):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)
    company = models.ForeignKey(User , on_delete = models.CASCADE , limit_choices_to = {"user_type":"company"})
    title = models.CharField(max_length = 100)
    category = models.ForeignKey(JobCategory , on_delete = models.SET_NULL , null = True , blank = True , related_name = "jobs")
    description = SummernoteTextField()

    max_salary = models.PositiveIntegerField(blank = True , null = True)
    min_salary = models.PositiveIntegerField(blank = True , null = True)
    location = models.CharField(max_length = 70 , blank = True , null = True)

    class JobTypeChoices(models.TextChoices):
        INTERN = "intern" , "Intern"
        FULL_TIME = "full_time" , "Full time"
        PART_TIME = "part_time" , "Part time"
        CONTRACT = "contract" , "Contract"
        REMOTE = "remote" , "Remote"
    job_type = models.CharField(max_length = 20 , choices = JobTypeChoices.choices)
    class ExperienceType(models.TextChoices):
        SENIOR = "senior" , "Senior"
        MID = "mid" , "Mid"
        JUNIOR = "junior" , "Junior"
    expericen = models.CharField(max_length = 6 , choices = ExperienceType.choices , default = ExperienceType.JUNIOR)
    vacancy = models.PositiveIntegerField(
        validators = [
            MinValueValidator(limit_value = 1 , message = "Vacancy must be equal or greater than 1"),
        ] , 
        default = 1
    )
    posted_at = models.DateTimeField(auto_now_add = True)
    deadline = models.DateTimeField(blank = True , null = True)

    is_active = models.BooleanField(default = True)

    objects = JobManager()

    def __str__(self):
        return f"{self.company} posted a new job "
    
    class Meta:
        indexes = [
            models.Index(fields = ["company"]),
            models.Index(fields = ["job_type"]),
            models.Index(fields = ["posted_at"]),
            models.Index(fields = ["category"]),
            models.Index(fields = ["is_active"]),
            models.Index(fields = ["is_active" , "job_type"]),
        ]
        ordering = ["-posted_at"]
