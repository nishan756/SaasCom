from .models import Comment
from saas_com.core.exceptions import ObjectNotFound


class CommentRepo:

    def get_user_comment(self , user , id):
        try:
            return Comment.objects.get(user = user , id= id)
        except Comment.DoesNotExist:
            raise ObjectNotFound("Comment not found")
    
    def get_comment_by_id(self , id):
        try:
            return Comment.objects.get(id = id)
        except Comment.DoesNotExist:
            raise ObjectNotFound("Comment not found")
    
    def get_comments(self , content_type , object_id):
        return Comment.objects.filter(content_type = content_type , object_id = object_id).select_related("user" , "parent").prefetch_related("children")
    
    def post_comment(self , comment):
        return comment.save()

    def reply_comment(self , user , parent , content , content_type):
        Comment.objects.create(
            user = user,
            parent = parent,
            content = content,
            content_type = content_type,
            object_id = parent.object_id
        )

    def delete_comment(self , comment):
        return comment.delete()


