from session.models import CustomUser
from django.core.exceptions import ValidationError
from django.test import TestCase


class TestCustomUser(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(first_name = "Ata Alahy" , last_name = "Nishan" , email = "aanishan339@gmailc.com" , username = "nishan000" , bio = "Dont judge me, till you know me" , user_type = "developer" , gender = "male")
        self.user.set_password("test_password")
        self.user.save()
    
    def test_invalid_user_type(self):
        self.user.user_type = "invalid"
        with self.assertRaises(ValidationError):
            self.user.full_clean()
    
    def test_invalid_gender_type(self):
        self.user.gender = "invalid"
        with self.assertRaises(ValidationError):
            self.user.full_clean()
    
    def test_user_is_not_superuser(self):
        self.assertTrue(not self.user.is_superuser)
    
    def test_user_is_superuser(self):
        self.user.is_superuser = True
        self.assertTrue(self.user.is_superuser)
    
    def test_user_is_active(self):
        self.assertTrue(self.user.is_active)
    
    def test_user_is_not_active(self):
        self.user.is_active = False
        self.assertTrue(not self.user.is_active)
    
    def test_user_is_developer(self):
        self.assertTrue(self.user.is_developer)
    
    def test_user_is_company(self):
        self.user.user_type = "company"
        self.assertTrue(self.user.is_company)

