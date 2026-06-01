from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django_summernote.fields import SummernoteTextField
import uuid

User = get_user_model()

class Comment(models.Model):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)
    author = models.ForeignKey(User , on_delete = models.CASCADE , related_name = "comments")
    parent = models.ForeignKey("self" , on_delete = models.CASCADE , blank = True , null = True , related_name = "children")
    content = SummernoteTextField()

    content_type = models.ForeignKey(ContentType , on_delete = models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type" , "object_id")

    posted_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ["-posted_at"]
        indexes = [
            models.Index(fields = ["author"]),
            models.Index(fields = ["content_type" , "object_id"]),
            models.Index(fields = ["posted_at"]),
            models.Index(fields = ["parent",]),
        ]

    def __str__(self):
        return f"Comment by {self.author} on {self.content_object}"