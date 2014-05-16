from django.test import TestCase
from django.test.client import Client
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Rol.models import Rol
from django.core.urlresolvers import reverse
# Create your tests here.

class TestUsuarioView(TestCase):

    def crear_usuario(self, nick, nombre= 'test', apellido='test', cedula='12345', email='test@test.com',password= 'test'):
        return Usuario.objects.create(nick=nick ,nombre= nombre, apellido=apellido, cedula=cedula, email=email,password= password)


    def test_crea_usuario(self):
        u = self.crear_usuario(nick='prueba')
        self.assertTrue(isinstance(u,Usuario))
        self.assertEqual(u.__unicode__(), u.nombre)
        print('Test de crear usuario, exitoso')


    def test_admin_usuario(self):
        usuario = Usuario.objects.create(nick='prueba')
        Rol(nombre= 'Administrador del Sistema', usuario=usuario)
        client = Client()
        response = client.post('/proyecto/usuario/mostrar/', {'login':usuario.pk, 'codigo':usuario.pk})
        self.assertEqual(response.status_code, 200)
        print('Test de mostrar usuario si tiene permiso, exitoso')