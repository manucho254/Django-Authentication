from django.test import TestCase
from django.test import Client

# Create your tests here.

class TestAuth(TestCase):
    
    def setUp(self) -> None:
        self.client = Client()