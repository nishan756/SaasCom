from django.db import models
import uuid
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.utils.timezone import now


User = get_user_model()


class Report(models.Model):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)
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

    def __str__(self):
        return f"Report by {self.reporter} to {self.content_type}-{self.object_id} for {self.report_type} "

    class Meta:
        unique_together = ["reporter" , "content_type" , "object_id"]
        indexes = [
            models.Index(fields = ["content_type" , "object_id"]),
            models.Index(fields = ["reporter"]),
            models.Index(fields = ["report_type"]),
            models.Index(fields = ["reported_at"])
        ]
