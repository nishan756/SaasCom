from session.models import Follow
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db.utils import IntegrityError

User = get_user_model()

class TestFollow(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username = "nishan000" , email = "user1@gmail.com")
        self.user1.set_password("nishan000")

        self.user1.save()

        self.user2 = User.objects.create(username = "junayed.iqbal" , email = "user2@gmail.com")
        self.user2.set_password("junayed.iqbal")

        self.user2.save()

        self.follow = Follow.objects.create(
            follower = self.user1,
            following = self.user2
        )
    
    def test__str__method(self):
        self.assertEqual(self.follow.__str__() , f"{self.user1}->{self.user2}")
    
    def test_fk_cannot_be_null(self):
        self.follow.follower = None
        with self.assertRaises(ValidationError):
            self.follow.full_clean()
    
    def test_cannot_duplicate_follow_object(self):
        with self.assertRaises(IntegrityError):
            Follow.objects.create(
                follower = self.user1,
                following = self.user2,
            )

