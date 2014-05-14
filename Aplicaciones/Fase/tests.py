from django.test import TestCase
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Proyecto.models import Proyecto
from .models import Fase
# Create your tests here.

class TestFaseView(TestCase):
    
    def crear_usuario(self,nick, nombre= 'test', apellido='test', cedula='12345', email='test@test.com',password= 'test'):
        return Usuario.objects.create(nick= nick,nombre= nombre, apellido=apellido, cedula=cedula, email=email,password= password)

    def crear_rol(self, nombre, u):
        return Rol(nombre = nombre, usuario = u)
    
    def crear_proyecto(self, nombre):
        w = self.crear_usuario(nick= 'liderU')
       # u = self.crear_rol(nombre ='Lider del Proyecto', usuario=w )
        P = Proyecto.objects.create(nombre = nombre, descripcion = 'Esto es una prueba',lider= w)
        return P

    def crear_fase(self, nombre):
        p = self.crear_proyecto(nombre='Proyecto_test')
        return Fase.objects.create(nombre= nombre, proyecto= p)

    def test_crea_fase(self):
        test = self.crear_fase(nombre ='test')
        self.assertTrue(isinstance(test,Fase))
        self.assertEqual(test.__unicode__(), test.nombre)
        print('Test de crear Fase, exitoso')
