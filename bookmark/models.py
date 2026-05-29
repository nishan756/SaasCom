from django.db import models
import uuid
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model

User = get_user_model()


class Bookmark(models.Model):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)
    user = models.ForeignKey(User , on_delete = models.CASCADE , related_name = "bookmarks")
    content_type = models.ForeignKey(ContentType , on_delete = models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type" , "object_id")
    bookmarked_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.content_type}->{self.object_id} bookmarked by {self.user}"

    class Meta:
        ordering = ["-bookmarked_at"]
        constraints = [
            models.UniqueConstraint(
                fields = ["user" , "content_type" , "object_id"],
                name = "unique_user_bookmark"
            )
        ]
        indexes = [
            models.Index(fields = ["user" , "content_type" , "object_id"]),
            models.Index(fields = ["user"]),
            models.Index(fields = ["user","content_type"])
        ]

