from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()



class EventType(models.TextChoices):

    JOB_POSTED = "JOB_POSTED", "Job posted"

    APPLICATION_SUBMITTED = "APPLICATION_SUBMITTED", "Application submitted"
    APPLICATION_ACCEPTED = "APPLICATION_ACCEPTED", "Application accepted"
    APPLICATION_REJECTED = "APPLICATION_REJECTED", "Application rejected"
    APPLICATION_SHORTLISTED = "APPLICATION_SHORTLISTED", "Application shortlisted"

    POST_CREATED = "POST_CREATED", "Post created"
    POST_VOTED = "POST_VOTED", "Post voted"
    POST_REVIEWED = "POST_REVIEWED", "Post reviewed"

    COMMENT_POSTED = "COMMENT_POSTED", "Comment posted"
    COMMENT_REPLIED = "COMMENT_REPLIED", "Comment replied"

    REPORT_ADDED = "REPORT_ADDED", "Report added"

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete = models.CASCADE , related_name = "notifications")

    actor = models.ForeignKey(User, on_delete = models.CASCADE , related_name = "notification_triggerer")

    event_type = models.CharField(
        max_length=50,
        choices=EventType.choices
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True
    )

    object_id = models.UUIDField(
        null=True
    )

    content_object = GenericForeignKey(
        "content_type",
        "object_id"
    )

    content = models.CharField(max_length = 300)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields = ["recipient" , "is_read"]),
            models.Index(fields = ["recipient"]),
            models.Index(fields = ["recipient" , "created_at" , "is_read"]),
        ]
