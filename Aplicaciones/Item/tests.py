from django.test import TestCase
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Proyecto.models import Proyecto
from Aplicaciones.Fase.models import Fase
from .models import Item
# Create your tests here.

class TestItemView(TestCase):
    
    def crear_usuario(self,nick, nombre= 'test', apellido='test', cedula='12345', email='test@test.com',password= 'test'):
        return Usuario.objects.create(nick= nick,nombre= nombre, apellido=apellido, cedula=cedula, email=email,password= password)

    def crear_rol(self, nombre, nick):
        u = self.crear_usuario(nick= nick)
        return Rol(nombre = nombre, usuario = u)
    
    def crear_proyecto(self, nombre):
        return Proyecto.objects.create(nombre = nombre, descripcion = 'Esto es una prueba')

    def crear_fase(self, nombre):
        p = self.crear_proyecto( nombre='ProyectoI')
        return Fase.objects.create(nombre= nombre, proyecto= p)

    def crear_item(self, nombre ):
        f = self.crear_fase(nombre= 'Fase_item')
        return Item.objects.create(nombre = nombre, fase = f)

    #def test_crea_item(self):
   #     test = self.crear_item(nombre ='test_item')
  #      self.assertTrue(isinstance(test,Item))
 #       self.assertEqual(test.__unicode__(), test.nombre)
#        print('Test de crear item, exitoso')
