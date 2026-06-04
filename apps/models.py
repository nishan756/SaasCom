from django.db import models
from django.core.exceptions import ValidationError
from django_summernote.fields import SummernoteTextField
from django.contrib.auth import get_user_model
import uuid
from cloudinary.models import CloudinaryField
from django.contrib.contenttypes.fields import GenericRelation
from vote.models import Vote
from django.core.validators import MinValueValidator , MaxValueValidator

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length = 20 , unique = True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def clean(self):
        if Category.objects.filter(name__iexact = self.name).exclude(pk = self.pk).exists():
            raise ValidationError("Category with this name is already exists")
    

class App(models.Model):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)
    founder = models.ForeignKey(User , on_delete = models.SET_NULL , null = True , related_name = "apps")
    name = models.CharField(max_length = 70)
    category = models.ManyToManyField(Category , related_name = "apps" , blank = True)
    logo = CloudinaryField("Logo" , folder = "saas_com/assets/images/app_logos")
    developed_at = models.DateField(blank = True , null = True)
    short_description = models.CharField(max_length = 200 , blank = True)
    detail = SummernoteTextField()

    class StatusChoice(models.TextChoices):
        PENDING = "pending","Pending"
        APPROVED = "approved","Approved"
        REJECTED = "rejected","Rejected"
    
    status = models.CharField(choices = StatusChoice.choices , max_length = 10 , default = StatusChoice.PENDING)
    votes = GenericRelation(Vote , related_query_name = "apps")
    added_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-added_at"]
        indexes = [
            models.Index(fields = ["added_at"]),
            models.Index(fields = ["status"]),
            models.Index(fields = ["founder"]),
        ]


class AppImages(models.Model):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)
    app = models.ForeignKey(App , on_delete = models.CASCADE , related_name = "app_images")
    image = CloudinaryField("App Image" , folder = "saas_com/assets/images/app_images")
    added_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.app.name} image"
    
    def clean(self):
        if AppImages.objects.filter(app = self.app).count() > 5:
            raise ValidationError("Maximum 5 images allowed per app ")

    class Meta:
        ordering = ["-added_at"]


class Review(models.Model):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)
    app = models.ForeignKey(App , on_delete = models.CASCADE , related_name = "reviews")
    user = models.ForeignKey(User , on_delete = models.CASCADE , related_name = "reviews")
    rating = models.PositiveIntegerField(
        validators = [
            MinValueValidator(limit_value = 1),
            MaxValueValidator(limit_value = 5)
        ],
        null = True
    )
    review = models.TextField()
    added_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user.username} reviewed to {self.app.name}"
    
    class Meta:
        ordering = ["-added_at"]
        unique_together = ["user" , "app"]
        indexes = [
            models.Index(fields = ["app" , "user"]),
        ]
