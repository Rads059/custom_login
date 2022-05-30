from django.test import TestCase
from custom_login.models import User
from django.db import models
from django.urls import reverse  
from . forms import LoginForm
class BasicTestCase(TestCase):
    def setUp(self):
        User.objects.create(email="rcdeveloper419@gmail.com",name="Rahul", password="890")

class EntryModelTest(TestCase):

    def test_string_representation(self):
        entry = User(email="rcdeveloper419@gmail.com")
        self.assertEqual(str(entry), entry.email)


    def test_login_view(self):  
        response = self.client.get(reverse("login:dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_Form_valid(self):
        form = LoginForm(data={'email': "rcdeveloper419@gmail.com", 'password': "890"})
        self.assertTrue(form.is_valid())