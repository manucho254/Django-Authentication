from django.test import TestCase
from django.test import Client, RequestFactory
from . import views
import logging

# Create your tests here.

class TestAuth(TestCase):
    
    def setUp(self) -> None:
        self.client = Client()
    
    def test_login(self):
        request = self.client.post("/login", data={"username": "", "password": ""})
        
        self.assertEqual(request.status_code, 301)