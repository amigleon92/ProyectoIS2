from django.test import TestCase
# Create your tests here.
from Aplicaciones.Fase.models import Fase
from Aplicaciones.Linea_Base.models import LineaBase
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Usuario.models import Usuario


class TestLineaBase(TestCase):
    def crear_usuario(self,nick, nombre= 'test', apellido='test', cedula='12345', email='test@test.com',password= 'test'):
         return Usuario.objects.create(nick= nick,nombre= nombre, apellido=apellido, cedula=cedula, email=email,password= password)

    def crear_rol(self, nombre, u, p):
          return Rol(nombre = nombre, usuario = u, proyecto=p)

    def crear_proyecto(self, nombre):
          w = self.crear_usuario(nick= 'liderU')
          P = Proyecto.objects.create(nombre = nombre, descripcion = 'Esto es una prueba', lider= w)
          u = self.crear_rol(nombre ='Lider del Proyecto', u= w , p=P)
          return P

    def crear_fase(self, nombre):
          p = self.crear_proyecto(nombre='Proyecto_test')
          return Fase.objects.create(nombre= nombre, proyecto= p)

    def crear_lineaBase(self, nombre):
        f= self.crear_fase(nombre='testLB')
        return LineaBase(nombre=nombre, fase=f)

    def test_crea_item(self):
         test = self.crear_lineaBase(nombre ='test_LB')
         self.assertTrue(isinstance(test,LineaBase))
         self.assertEqual(test.__unicode__(), test.nombre)
         print('Test de crear Linea Base, exitoso')