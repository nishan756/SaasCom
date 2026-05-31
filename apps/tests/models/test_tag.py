from apps.models import Tag
from django.core.exceptions import ValidationError
from django.test import TestCase


class TestTag(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(title = "django")
    
    def test_str_method(self):
        self.assertEqual(self.tag.__str__() , "django")
    
    def test_clean_duplicate_raises_error(self):
        tag = Tag(title = "django")
        with self.assertRaises(ValidationError):
            tag.full_clean()
    
    def test_clean_valid_data_passes(self):
        tag = Tag(title = "drf")
        tag.full_clean()