from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

class Vote(models.Model):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)
    user = models.ForeignKey(User , on_delete = models.CASCADE , related_name = "votes")
    class VoteChoice(models.TextChoices):
        UPVOTE = "upvote" , "Up Vote"
        DOWNVOTE = "downvote" , "Down Vote"
    
    vote_type = models.CharField(max_length = 12 , choices = VoteChoice.choices)
    content_type = models.ForeignKey(ContentType , on_delete = models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")
    
    added_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user.username} voted to {self.content_type}"
    
    class Meta:
        ordering = ["-added_at"]
        unique_together = ["user" , "content_type" , "object_id"]
        indexes = [
            models.Index(fields = ["user"]),
            models.Index(fields = ["content_type" , "object_id"]),
            models.Index(fields = ["user" , "content_type" , "object_id"]),
        ]
