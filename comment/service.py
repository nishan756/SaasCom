from .repository import CommentRepo
from discussion.models import Discussion
from saas_com.core.exceptions import InvalidForm , InvalidContentType , ObjectNotFound
from saas_com.core.service import get_content_type
from django.db.models import QuerySet


class CommentService:
    repo = CommentRepo()
    CONTENT_TYPES = {
        "discussion":Discussion,
    }

    def get_user_comment(self , user , id):
        return self.repo.get_user_comment(user = user , id = id)

    def get_comment_by_id(self , id):
        return self.repo.get_comment_by_id(id)
    
    def get_comments(self , content_type_str , object_id):
        content_type_obj = get_content_type(content_type_str , self.CONTENT_TYPES)
        return self.repo.get_comments(content_type_obj , object_id)
    
    def build_comment_tree(self , comments:QuerySet):
        root_comments = []
        comment_map = {}
        length = comments.count()

        for comment in comments:
            comment.childrens = []
            comment_map[comment.id] = comment
        
        for comment in comments:

            if comment.parent_id:
                parent = comment_map[comment.parent_id]
                parent.childrens.append(comment)
            else:
                root_comments.append(comment)

        return {"root_comments":root_comments , "length":length}
    
    def post_comment(self , user , content_type_str , object_id , form , parent_id = None):
        content_type_obj = get_content_type(content_type_str , self.CONTENT_TYPES)
        if not form.is_valid():
            raise InvalidForm(form.errors)
        
        comment = form.save(commit = False)
        comment.content_type = content_type_obj
        comment.object_id = object_id
        comment.user = user
        return self.repo.post_comment(comment)
    
    def reply_comment(self , user , parent_id , content):
        parent = self.get_comment_by_id(parent_id)
        return self.repo.reply_comment(user , parent , content)
    
    def delete_comment(self , user , id):
        return self.repo.delete_comment(self.get_user_comment(user , id))
