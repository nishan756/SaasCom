from django.db import models
import uuid
from cloudinary.models import CloudinaryField
from django_summernote.fields import SummernoteTextField
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from vote.models import Vote
from comment.models import Comment

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length = 30)
    def __str__(self):
        return self.title
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["title"],
                name = "unique_title_constrain"
            )
        ]

class Discussion(models.Model):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)
    user = models.ForeignKey(User , on_delete = models.CASCADE , related_name = "discussions")
    title = models.CharField(max_length = 120)
    banner = CloudinaryField(blank = True , null = True)
    tags = models.ManyToManyField(Tag , blank = True , related_name = "discussions")
    short_description = models.TextField(max_length = 200)
    detail = SummernoteTextField()

    votes = GenericRelation(Vote , related_query_name = "discussions")
    comments = GenericRelation(Comment , related_query_name = "comments")

    posted_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ["-posted_at"]
        indexes = [
            models.Index(fields = ["user"]),
            models.Index(fields = ["posted_at"]),
        ]

