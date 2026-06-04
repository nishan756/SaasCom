from .models import Comment
from saas_com.core.exceptions import ObjectNotFound


class CommentRepo:

    def get_author_comment(self , author , id):
        try:
            return Comment.objects.get(author = author , id= id)
        except Comment.DoesNotExist:
            raise ObjectNotFound("Comment not found")
    
    def get_comment_by_id(self , id):
        try:
            return Comment.objects.get(id = id)
        except Comment.DoesNotExist:
            raise ObjectNotFound("Comment not found")
    
    def get_comments(self , content_type , object_id):
        return Comment.objects.filter(content_type = content_type , object_id = object_id).select_related("author" , "parent")
    
    def post_comment(self , comment):
        return comment.save()

    def delete_comment(self , comment):
        return comment.delete()


