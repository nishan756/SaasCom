from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager , PermissionsMixin
import uuid
from cloudinary.models import CloudinaryField
from django.utils.timezone import now
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class CustomUserManager(BaseUserManager):

    def _create_user(self, username=None, email=None, password=None, **extra_fields):

        if not email:
            raise ValueError("Users must have an email address")

        if not password:
            raise ValueError("Password must be provided")

        if not username:
            raise ValueError("Username must be provided")

        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):

        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        return self._create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser , PermissionsMixin):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)

    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    image = CloudinaryField("User Image" , folder = "saas_com/assets/images/user_images" , blank = True , null = True)

    username = models.CharField(max_length = 30 , unique = True)
    email = models.EmailField(unique = True)

    class GenderChoices(models.TextChoices):
        MALE = "male" , "Male"
        FEMALE = "female" , "Female"
        THIRD = "Third" , "third"
        TRANSGENDER = "transgender" , "Transgender"
    gender = models.CharField(max_length = 12 , default = GenderChoices.MALE , choices = GenderChoices.choices)
    date_of_birth = models.DateField(blank = True , null = True)

    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_superuser = models.BooleanField(default = False)

    objects = CustomUserManager()

    joined_at = models.DateTimeField(default = now)

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = [
        "email",
    ]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


from django.contrib.auth import get_user_model
User = get_user_model()

class Follow(models.Model):
    follower = models.ForeignKey(
        User , 
        on_delete = models.CASCADE , 
        related_name = "following",
    )
    following = models.ForeignKey(
        User , 
        on_delete = models.CASCADE , 
        related_name = "followers",
    )

    class Meta:
        unique_together = ["follower" , "following"]
        indexes = [
            models.Index(fields = ["following"]),
            models.Index(fields = ["follower"]),
        ]

class Report(models.Model):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)
    reported_profile = models.ForeignKey(User , on_delete = models.CASCADE , related_name = "reports")
    reporter = models.ForeignKey(User , on_delete = models.CASCADE , related_name = "my_reports")

    class ReportTypeChoices(models.TextChoices):
        SPAM = "spam", "Spam",
        FAKE = "fake", "Fake Information",
        HARASSMENT = "harassment", "Harassment",
        COPYRIGHT = "copyright", "Copyright",
        NSFW = "nsfw", "NSFW",
        SCAM = "scam", "Scam",
        OTHER = "other", "Other",
    
    report_type = models.CharField(max_length = 20 , choices = ReportTypeChoices.choices , blank = True , null = True)
    reason = models.TextField(blank = True , null = True)
    reported_at = models.DateTimeField(default = now)

    content_type = models.ForeignKey(ContentType , on_delete = models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __init__(self):
        return f"Report by {self.reporter.username} to {self.reported_profile.username}"

    class Meta:
        unique_together = ["reporter" , "content_type" , "object_id"]
        indexes = [
            models.Index(fields = ["content_type" , "object_id"]),
            models.Index(fields = ["reporter"]),
            models.Index(fields = ["report_type"]),
            models.Index(fields = ["reported_at"])
        ]

