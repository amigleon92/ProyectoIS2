from django.test import TestCase
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Rol.models import Rol
from django.core.urlresolvers import reverse
# Create your tests here.

class TestRolView(TestCase):

    def crear_usuario(self,nick, nombre= 'test', apellido='test', cedula='12345', email='test@test.com',password= 'test'):
        return Usuario.objects.create(nick= nick,nombre= nombre, apellido=apellido, cedula=cedula, email=email,password= password)

    def crear_rol(self, nombre):
        u = self.crear_usuario(nick='test')
        return Rol(nombre = nombre, usuario = u)

    def test_crea_rol(self):
        u = self.crear_rol(nombre ='test')
        self.assertTrue(isinstance(u,Rol))
        self.assertEqual(u.__unicode__(), u.nombre)
        print('Test de crear rol, exitoso')

#    def test_rol_view(self):
 #       w = self.crear_usuario(nick= 'admin')
  #      u = self.crear_rol(nombre ='Administrador del Sistema')
   #     url = reverse("/Aplicaciones.Rol.views.RolView")
    #    print('url obtiene: ', url)
     #   resp = self.client.get(url)

#        print('resp obtiene', resp)



 #       self.assertEqual(resp.status_code, 200)
  #      self.assertIn(w.title, resp.content)
   #     print('Test de crear rol si permiso, exitoso')