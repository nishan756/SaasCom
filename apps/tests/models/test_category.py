from django.test import TestCase
from apps.models import Category
from django.core.exceptions import ValidationError

class TestCategory(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name = "AI")
    
    def test__str__repr(self):
        self.assertEqual(self.category.__str__() , "AI")

    def test_clean_duplicate_raises_error(self):
        category = Category(name = "AI")
        with self.assertRaises(ValidationError):
            category.full_clean()
    
    def test_clean_valid_data_passes(self):
        category = Category(name = "SaaS")
        category.full_clean()