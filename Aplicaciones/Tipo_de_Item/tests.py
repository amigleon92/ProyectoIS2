from unittest import TestCase
from django.test import TestCase
from Aplicaciones.Fase.models import Fase
from Aplicaciones.Linea_Base.models import LineaBase
from Aplicaciones.Tipo_de_Item.models import Tipo_de_Item
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Proyecto.models import Proyecto
# Create your tests here.
class TestTipo_de_Item(TestCase):

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

     def crear_tipo_item(self, nombre):
          p = self.crear_proyecto(nombre='Proyecto_test')
          return Tipo_de_Item.objects.create(nombre= nombre, descripcion= 'Item Tipo test', cantidad_de_item=1, proyecto= p)

     def test_crea_tipoItem(self):
         test = self.crear_tipo_item(nombre ='test')
         self.assertTrue(isinstance(test,Tipo_de_Item))
         self.assertEqual(test.__unicode__(), test.nombre)
         print('Test de crear Tipo de Item, exitoso')