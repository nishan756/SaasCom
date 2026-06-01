from comment.models import Comment
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from discussion.models import Discussion
from django.core.exceptions import ValidationError

User = get_user_model()

class TestComment(TestCase):

    def setUp(self):
        self.author = User.objects.create(username = 'razoan' , password = 'razoan')
        self.content_type = ContentType.objects.get_for_model(model = Discussion)
        self.discussion = Discussion.objects.create(author = self.author , title = "test" , short_description = "test" , detail = "test")
        self.comment = Comment.objects.create(
            author = self.author,
            content_type = self.content_type,
            object_id = self.discussion.id,
            content = "test_content"
        )
    
    def test_str_method(self):
        self.assertEqual(f"Comment by {self.author} on {self.content_type}" , "Comment by razoan on Discussion | discussion")
    
    def test_object_not_found_while_fk_user_is_none(self):
        comment_id = self.comment.id
        self.author.delete()
        self.assertFalse(Comment.objects.filter(id = comment_id).exists())
    
    def test_parent_is_null(self):
        self.assertTrue(not self.comment.parent)
    
    def test_parent_exists(self):
        comment = Comment.objects.create(
            author = self.author,
            content_type = self.content_type,
            object_id = self.discussion.id,
            content = "test_content"
        )
        self.comment.parent = comment
        self.assertTrue(self.comment.parent)