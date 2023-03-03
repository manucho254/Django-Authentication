from django.test import TestCase
from django.test import Client

# Create your tests here.

class TestAuth(TestCase):
    
    def setUp(self) -> None:
        self.client = Client()
        return super().setUp()
    
    def test_login(self):
        login_user = self.client.post("/login", data={"username": "", "password": ""})
        self.assertEqual(login_user.status_code == 400)