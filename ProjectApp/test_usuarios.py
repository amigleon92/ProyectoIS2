from unittest import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
__author__ = 'choffis'


class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'prueba'
        self.email = 'test@test.com'
        self.password = 'prueba'
        self.test_user = User.objects.create_user(self.username, self.email, self.password)

    def test_login_exitoso(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertEqual(login, True)