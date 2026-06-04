from .repository import CommentRepo
from discussion.models import Discussion
from saas_com.core.exceptions import InvalidForm , InvalidContentType , ObjectNotFound
from saas_com.core.service import get_content_type


class CommentService:
    repo = CommentRepo()
    CONTENT_TYPES = {
        "discussion":Discussion,
    }

    def get_author_comment(self , author , id):
        return self.repo.get_author_comment(author = author , id = id)

    def get_comment_by_id(self , id):
        return self.repo.get_comment_by_id(id)
    
    def get_comments(self , content_type , object_id):
        content_type = get_content_type(content_type , self.CONTENT_TYPES)
        return self.repo.get_comments(content_type , object_id)

    def post_comment(self , author , content_type , object_id , form , parent_id = None):
        content_type = get_content_type(content_type , self.CONTENT_TYPES)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.content_type = content_type
            comment.object_id = object_id
            comment.author = author
            if parent_id:
                comment.parent = self.get_comment_by_id(parent_id)
            return self.repo.post_comment(comment)
        raise InvalidForm("Invalid form data")
    
    def delete_comment(self , author , id):
        return self.repo.delete_comment(self.get_author_comment(author , id))
