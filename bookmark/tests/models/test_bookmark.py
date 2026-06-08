from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from bookmark.models import Bookmark
from discussion.models import Discussion
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

User = get_user_model()



class TestBookmark(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username = "username" , password = "password" , user_type = "company" , email = "user1@gmail.com")

        # self.user2 = User.objects.create(username = "username2" , password = "password2" , user_type = "company" , email = "user2@gmail.com")

        self.discussion = Discussion.objects.create(title = "test title" , short_description = "test" , detail = "test" , user = self.user1)

        self.content_type = ContentType.objects.get_for_model(Discussion)
        self.bookmark = Bookmark.objects.create(user = self.user1 , content_type = self.content_type , object_id = self.discussion.id)
    
    def test__str__method(self):
        self.assertEqual(self.bookmark.__str__() , f"{self.content_type}->{self.discussion.id} bookmarked by {self.user1}")
    
    
    def test_content_type(self):
        self.assertEqual(self.bookmark.content_type.model , "discussion")
    
    def test_content_type_cannot_null(self):
        self.bookmark.content_type = None
        with self.assertRaises(ValidationError):
            self.bookmark.full_clean()
    
    
    def test_object_id_cannot_be_null(self):
        self.bookmark.object_id = None
        with self.assertRaises(ValidationError):
            self.bookmark.full_clean()
    
    def test_user_cannot_bookmark_twice_for_same_obj(self):

        with self.assertRaises(IntegrityError):
            Bookmark.objects.create(user = self.user1 , content_type = self.content_type , object_id = self.discussion.id)
    