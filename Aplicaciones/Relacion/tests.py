
from django.test import TestCase, Client

# Create your tests here.
from Aplicaciones.Fase.models import Fase
from Aplicaciones.Item.models import Item
from Aplicaciones.Linea_Base.models import LineaBase
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Relacion.models import Relacion
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Tipo_de_Item.models import Tipo_de_Item
from Aplicaciones.Usuario.models import Usuario


class TestRelacion(TestCase):

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


    def crear_relacion(self, nombre):
        item1 = self.crear_item(nombre= 'itemI', nombrelB='LineaBI', nombreF='FaseI', nombreP='ProyectoI', nombreU='UsuarioI')
        item2 = self.crear_item(nombre= 'itemII',nombrelB='LineaBII', nombreF='FaseII', nombreP='ProyectoII', nombreU='UsuarioII')
        #  crear una relacion sin items
        return Relacion.objects.create(nombre= nombre, item1= item1, item2= item2, tipo= 'A/S')

    def crear_relacion_sin_item(self, nombre):
        return Relacion.objects.create(nombre= nombre, tipo= 'A/S')

    def test_crea_relacion(self):
         test = self.crear_relacion(nombre ='test_relacion')
         self.assertTrue(isinstance(test,Relacion))
         self.assertEqual(test.__unicode__(), test.nombre)
         print('Test de crea relacion, exitoso')

    def test_crea_relacion_sin_item(self):
         test = self.crear_relacion_sin_item(nombre ='relacion_vacia')
         self.assertTrue(isinstance(test,Relacion))
         self.assertEqual(test.__unicode__(), test.nombre)
         print('Test de crea relacion vacia, exitoso')

    def crear_relacion_ciclica(self, nombre):
        item1 = self.crear_item(nombre= 'itemI', nombrelB='LineaBI', nombreF='FaseI', nombreP='ProyectoI', nombreU='UsuarioI')
        # crear una relacion sin items
        return Relacion.objects.create(nombre= nombre, item1= item1, item2= item1, tipo= 'A/S')

    def test_crea_relacion_ciclos(self):
         test = self.crear_relacion_ciclica(nombre ='relacion_ciclica')
         self.assertTrue(isinstance(test,Relacion))
         self.assertEqual(test.__unicode__(), test.nombre)
         print('Test de crea relacion ciclica, exitoso')

    def test_relacion_confirmarAS(self):
        relacion = self.crear_relacion_ciclica(nombre='relacionrara')
        client = Client()
        response = client.post('/proyecto/fase/item/relacion/establecerRelacionAS/Confirmar/', {'login':relacion.item1.fase.proyecto.lider.pk, 'proyecto':relacion.item1.fase.proyecto.pk, 'fase':relacion.item1.fase.pk, 'item':relacion.item1.pk, 'item2':relacion.item2.pk, 'nombre_relacion':relacion.nombre})
        print(response.context['error'])
        self.assertEqual(response.status_code, 200)
        print('Test control de relacion, exitoso')