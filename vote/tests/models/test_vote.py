from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from discussion.models import Discussion , Tag
from django.contrib.auth import get_user_model
from vote.models import Vote
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

User = get_user_model()



class TestVote(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username = "username" , password = "password" , user_type = "company" , email = "user1@gmail.com")
        self.user2 = User.objects.create(username = "username2" , password = "password2" , user_type = "company" , email = "user2@gmail.com")

        self.tag = Tag.objects.create(title = "title")
        self.discussion = Discussion.objects.create(title = "test title" , short_description = "test" , detail = "test" , user = self.user1)
        self.discussion.tags.add(self.tag)

        self.content_type = ContentType.objects.get_for_model(Discussion)
        self.vote = Vote.objects.create(vote_type = "upvote" , user = self.user2 , content_type = self.content_type , object_id = self.discussion.id)
    
    def test_vote_type(self):
        self.assertEqual(self.vote.vote_type , "upvote")
    
    def test_invaid_vote_type(self):
        self.vote.vote_type = "uvote"
        with self.assertRaises(ValidationError):
            self.vote.full_clean()
    
    def test_content_type(self):
        self.assertEqual(self.content_type.model , "discussion")

    def test_content_type_cannot_be_null(self):
        self.vote.content_type = None
        with self.assertRaises(ValidationError):
            self.vote.full_clean()
    
    def test_object_id_cannot_be_null(self):
        self.vote.object_id = None
        with self.assertRaises(ValidationError):
            self.vote.full_clean()
    
    def test_user_cannot_vote_twice(self):

        with self.assertRaises(IntegrityError):
            Vote.objects.create(vote_type = "upvote" , user = self.user2 , content_type = self.content_type , object_id = self.discussion.id)

    
    
