from django.test import TestCase
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Proyecto.models import Proyecto
# Create your tests here.

class TestProyectoView(TestCase):

    def crear_usuario(self,nick, nombre= 'test', apellido='test', cedula='12345', email='test@test.com',password= 'test'):
        return Usuario.objects.create(nick= nick,nombre= nombre, apellido=apellido, cedula=cedula, email=email,password= password)

    def crear_rol(self, nombre, usuario):
        return Rol(nombre = nombre, usuario = usuario)

    def crear_proyecto(self, nombre):
        w = self.crear_usuario(nick= 'liderU')
        u = self.crear_rol(nombre ='Lider del Proyecto', usuario=w )
        P = Proyecto.objects.create(nombre = nombre, descripcion = 'Esto es una prueba',lider= w)
        return (P)

    def test_crea_proyecto(self):
        u = self.crear_proyecto(nombre ='test')
        self.assertTrue(isinstance(u , Proyecto))
        self.assertEqual(u.__unicode__(), u.nombre)
        print('Test de crear proyecto, exitoso')
