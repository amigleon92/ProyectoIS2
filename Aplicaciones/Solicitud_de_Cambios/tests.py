from unittest import TestCase
from django.test import TestCase

# Create your tests here.
from Aplicaciones.Fase.models import Fase
from Aplicaciones.Item.models import Item
from Aplicaciones.Linea_Base.models import LineaBase
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Solicitud_de_Cambios.models import Solicitud_de_Cambios
from Aplicaciones.Tipo_de_Item.models import Tipo_de_Item
from Aplicaciones.Usuario.models import Usuario


class TestSolicitud_de_Cambios(TestCase):

    def crear_usuario(self,nick, nombre= 'test', apellido='test', cedula='12345', email='test@test.com',password= 'test'):
         return Usuario.objects.create(nick= nick,nombre= nombre, apellido=apellido, cedula=cedula, email=email,password= password)

    def crear_rol(self, nombre, u, p):
          return Rol(nombre = nombre, usuario = u, proyecto=p)

    def crear_proyecto(self, nombre, nick):
          w = self.crear_usuario(nick= nick)
          P = Proyecto.objects.create(nombre = nombre, descripcion = 'Esto es una prueba', lider= w)
          u = self.crear_rol(nombre ='Lider del Proyecto', u= w , p=P)
          return P

    def crear_fase(self, nombre, nombreP, nombreU):
          p = self.crear_proyecto(nombre=nombreP, nick=nombreU)
          return Fase.objects.create(nombre= nombre, proyecto= p)

    def crear_tipo_item(self, nombre, p):
          return Tipo_de_Item.objects.create(nombre= nombre, descripcion= 'Item Tipo test', cantidad_de_item=1, proyecto= p)

    def crear_lineaBase(self, nombre, nombreF, nombreP, nombreU ):
        f= self.crear_fase(nombre=nombreF, nombreP=nombreP, nombreU=nombreU)
        return LineaBase(nombre=nombre, fase=f)

    def crear_item(self, nombre, nombrelB, nombreF, nombreP, nombreU):
         LB = self.crear_lineaBase(nombre= nombrelB,nombreF=nombreF, nombreP=nombreP, nombreU=nombreU)
         tipo_item= self.crear_tipo_item(nombre='tipo', p=LB.fase.proyecto)
         return Item.objects.create(nombre = nombre,prioridad=1,  tipodeItemAsociado= tipo_item.nombre, tipo_de_item= tipo_item, fase=LB.fase, lineaBase=LB)

    def crear_solicitud(self, descrip, proyect, faseP, Us, nLineaB, item_name):
        item= self.crear_item(nombre=item_name, nombrelB=nLineaB, nombreF=faseP, nombreP=proyect, nombreU=Us)
        return Solicitud_de_Cambios.objects.create(descripcion= descrip, proyecto=item.fase.proyecto, fase=item.fase, item_sc_aprobado=item, item_sc_desaprobado=item,usuario= item.fase.proyecto.lider)

    def test_crea_relacion_ciclos(self):
         test = self.crear_solicitud(descrip='esto es una solicitud', proyect='proyecto', faseP='fase', Us='us', nLineaB='Linea de solicitud',item_name='item_a_cambiar')
         self.assertTrue(isinstance(test, Solicitud_de_Cambios))
         self.assertEqual(test.__unicode__(), test.descripcion)
         print('Test de crea solicitud, exitoso')
