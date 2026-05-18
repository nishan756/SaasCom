from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django_summernote.fields import SummernoteTextField
from django.core.exceptions import ValidationError

User = get_user_model()


class JobCategory(models.Model):
    title = models.CharField(max_length = 100 , unique = True)
    parent = models.ForeignKey("self" ,on_delete = models.CASCADE , blank = True , null = True , related_name = "sub_categories")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]


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

    posted_at = models.DateTimeField(auto_now_add = True)
    deadline = models.DateTimeField(blank = True , null = True)

    is_active = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.company} posted a new job "

    def clean(self):
        if self.deadline and self.deadline < self.posted_at:
            raise ValidationError("Deadline can\'t be in the past")
    class Meta:
        indexes = [
            models.Index(fields = ["company"]),
            models.Index(fields = ["job_type"]),
            models.Index(fields = ["posted_at"]),
            models.Index(fields = ["category"]),
        ]

