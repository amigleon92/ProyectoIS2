from django.test import TestCase
from Aplicaciones.Usuario.models import Usuario
from django.core.urlresolvers import reverse
# Create your tests here.

class TestUsuarioView(TestCase):

    def crear_usuario(self, nick='test',nombre= 'test', apellido='test', cedula='12345', email='test@test.com',password= 'test'):
        return Usuario.objects.create(nick=nick ,nombre= nombre, apellido=apellido, cedula=cedula, email=email,password= password)


    def test_crea_usuario(self):
        u = self.crear_usuario()
        self.assertTrue(isinstance(u,Usuario))
        self.assertEqual(u.__unicode__(), u.nombre)
        print('Test de crear usuario, exitoso')

#    def test_admin_usuario(self):
 #       w = self.crear_usuario()
  #      url = reverse("Aplicaciones.Usuario.views.MostrarUsuario")
   #     print('url obtiene: ', url)
    #    resp = self.client.get(url)

     #   print('resp obtiene', resp)
#
 #       self.assertEqual(resp.status_code, 200)
  #      self.assertIn(w.title, resp.content)
   #     print('Test de mostrar usuario si tiene permiso, exitoso')
