from unittest import TestCase
from django.test import TestCase

# Create your tests here.
from Aplicaciones.Fase.models import Fase
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Tipo_de_Atributo.models import Tipo_de_Atributo
from Aplicaciones.Tipo_de_Item.models import Tipo_de_Item
from Aplicaciones.Usuario.models import Usuario


class TestTipo_de_Atributo(TestCase):

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

     def crear_tipo_atributo(self, nombre):
         t_item = self.crear_tipo_item(nombre='test_t_atributo')
         return Tipo_de_Atributo(nombre=nombre, tipo_de_item= t_item)

     def test_crea_tipoAtributo(self):
         test = self.crear_tipo_atributo(nombre ='test')
         self.assertTrue(isinstance(test,Tipo_de_Atributo))
         self.assertEqual(test.__unicode__(), test.nombre)
         print('Test de crear Tipo de Atributo, exitoso')