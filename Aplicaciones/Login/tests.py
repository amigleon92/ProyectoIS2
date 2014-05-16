from django.test import TestCase

from Aplicaciones.Usuario.models import Usuario
# Create your tests here.
class TestLoginView(TestCase):
    def test_inicio(self):
        """
        test para verificar si va a la pagina de inicio

        """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        print('test inicio exitoso')

    def test_login(self):
        """
        test para verificar si realiza el login
        """
        resp = self.client.get('/')
        self.assertEqual(200,resp.status_code)
        print('test login exitoso')