from django.test import TestCase

# Create your tests here.
from Aplicaciones.Atributo.models import Atributo
from Aplicaciones.Fase.models import Fase
from Aplicaciones.Item.models import Item
from Aplicaciones.Linea_Base.models import LineaBase
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Tipo_de_Atributo.models import Tipo_de_Atributo
from Aplicaciones.Tipo_de_Item.models import Tipo_de_Item
from Aplicaciones.Usuario.models import Usuario


class TestAtributo(TestCase):
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

     def crear_tipo_item(self, nombre, p):
          return Tipo_de_Item.objects.create(nombre= nombre, descripcion= 'Item Tipo test', cantidad_de_item=1, proyecto= p)

     def crear_lineaBase(self, nombre):
        f= self.crear_fase(nombre='Fase_item')
        return LineaBase(nombre=nombre, fase=f)

     def crear_item(self, nombre ):
         LB = self.crear_lineaBase(nombre= 'lb_test_item')
         tipo_item= self.crear_tipo_item(nombre='tipo', p=LB.fase.proyecto)
         return Item.objects.create(nombre = nombre,prioridad=1,  tipodeItemAsociado= tipo_item.nombre, tipo_de_item= tipo_item, fase=LB.fase, lineaBase=LB)

     def crear_tipo_atributo(self, nombre, t_item):
         return Tipo_de_Atributo(nombre=nombre, tipo_de_item= t_item)

     def crear_atributo(self, nombre):
         item= self.crear_item(nombre='testItemAtributo')
         tipo_atri= self.crear_tipo_atributo(nombre='tipoAtributo_test', t_item=item.tipo_de_item)
         return Atributo.objects.create(nombre=nombre, descripcion='test atributo', tipo_de_atributo_nombre=tipo_atri.nombre, tipo_de_atributo_tipo=tipo_atri.tipo, item=item)

     def test_crea_Atributo(self):
         test = self.crear_atributo(nombre ='test')
         self.assertTrue(isinstance(test,Atributo))
         self.assertEqual(test.__unicode__(), test.nombre)
         print('Test de crear Atributo, exitoso')


