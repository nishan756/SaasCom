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
    
    def get_comments(self , content_type , object_id , **query_param):
        comments =  Comment.objects.filter(content_type = content_type , object_id = object_id).select_related("user" , "parent").prefetch_related("children")

        date_from = query_param.get("date_from" , None)
        date_to = query_param.get("date_to" , None)

        if date_from and date_to:
            comments = comments.filter(posted_at__gte = date_from , posted_at__lte = date_to)
        
        elif date_from:
            comments = comments.filter(posted_at__gte = date_from)
        
        elif date_to:
            comments = comments.filter(posted_at__lte = date_to)
        
        return comments
    
    def post_comment(self , comment):
        return comment.save()

    def reply_comment(self , user , parent , content):
        Comment.objects.create(
            user = user,
            parent = parent,
            content = content,
            content_type = parent.content_type,
            object_id = parent.object_id
        )

    def delete_comment(self , comment):
        return comment.delete()


