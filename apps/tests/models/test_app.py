from apps.models import App , User , Tag , Category
from django.core.exceptions import ValidationError
from django.test import TestCase


class TestApp(TestCase):
    
    def setUp(self):
        self.founder = User.objects.create(username = "nishan111" , password = "nishan111")
        self.tag = Tag.objects.create(title = "django")
        self.category = Category.objects.create(name = "AI")
        self.app = App.objects.create(name = "my_app" , founder = self.founder , short_description = "bla bla bla" , detail = "bla bla bla")
    
    def test_str_method(self):
        self.assertEqual(str(self.app) , "my_app")
    
    def test_default_status(self):
        self.assertEqual(self.app.status , "pending")
    
    def test_status(self):
        self.app.status = "published"
        self.app.save()
        self.assertEqual(self.app.status , "published")
    
    def test_invalid_status(self):
        app = App.objects.create(founder = self.founder , name = "app" , status = "invalid")
        with self.assertRaises(ValidationError):
            app.full_clean()
    
    def test_m2m_relations(self):
        self.app.category.add(self.category)
        self.app.tags.add(self.tag)

        self.assertIn(self.category , self.app.category.all())
        self.assertIn(self.tag , self.app.tags.all())
    
    def test_ordering(self):
        app2 = App.objects.create(founder = self.founder , name = "app2")
        apps = list(App.objects.all())

        self.assertEqual(apps[0] , app2)
    
    def test_fk_user_null(self):
        self.founder.delete()
        self.app.refresh_from_db()

        self.assertIsNone(self.app.founder)
    
    def test_full_clean(self):
        self.app.full_clean()
    