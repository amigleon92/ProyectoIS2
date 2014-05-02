from django.shortcuts import render
from Aplicaciones.Proyecto.views import ProyectoView
from .models import Usuario
from Aplicaciones.Rol.models import Rol
from Aplicaciones.Proyecto.models import Proyecto

# Create your views here.
#Lista de usuarios
class UsuarioView(ProyectoView):
    template_name = 'Usuario/Usuario.html'
    context_object_name = 'lista_usuarios'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        #Solamente el Administrador del Sistema puede ingresar a la Administracion de Usuarios
        if len(Rol.objects.filter(nombre= 'Administrador del Sistema', usuario= usuario_logueado)):
            diccionario[self.context_object_name]= Usuario.objects.order_by('id')
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No posee permisos para ver los usuarios del sistema'
            diccionario[super(UsuarioView, self).context_object_name]= Proyecto.objects.filter(activo= True)
            return render(request, super(UsuarioView, self).template_name, diccionario)

#Creacion de usuario
class CrearUsuario(UsuarioView):
    template_name = 'Usuario/CrearUsuario.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        return render(request, self.template_name, diccionario)

class CrearUsuarioConfirm(CrearUsuario):
    template_name = 'Usuario/CrearUsuarioConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        nuevo_nick= request.POST['user']
        existe= Usuario.objects.filter(nick= nuevo_nick)
        if len(existe):
            diccionario['error']= 'El nombre de usuario ya existe'
            return render(request, super(CrearUsuarioConfirm, self).template_name, diccionario)
        nuevo_usuario= Usuario()
        nuevo_usuario.nick= nuevo_nick
        nuevo_usuario.password= request.POST['pass']
        nuevo_usuario.nombre= request.POST['nombre']
        nuevo_usuario.apellido= request.POST['apellido']
        nuevo_usuario.cedula= request.POST['cedula']
        nuevo_usuario.email= request.POST['email']
        nuevo_usuario.save()
        return render(request, self.template_name, diccionario)

class EditarUsuario(UsuarioView):
    template_name = 'Usuario/EditarUsuario.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        diccionario['usuario']= Usuario.objects.get(id= request.POST['codigo'])
        return render(request, self.template_name, diccionario)

class EditarUsuarioConfirm(EditarUsuario):
    template_name = 'Usuario/EditarUsuarioConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        modificacion= Usuario.objects.get(id= request.POST['codigo'])
        modificacion_nick= request.POST['user']
        existe= Usuario.objects.filter(nick= modificacion_nick)
        if len(existe) and existe[0]!=modificacion:
            diccionario['error']= 'El nombre de usuario ya existe'
            diccionario['usuario']= modificacion
            return render(request, super(EditarUsuarioConfirm, self).template_name, diccionario)
        modificacion.nick= modificacion
        modificacion.password= request.POST['pass']
        modificacion.nombre= request.POST['nombre']
        modificacion.apellido= request.POST['apellido']
        modificacion.cedula= request.POST['cedula']
        modificacion.email= request.POST['email']
        modificacion.save()
        return render(request, self.template_name, diccionario)

class EliminarUsuario(UsuarioView):
    template_name = 'Usuario/EliminarUsuario.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        eliminado= Usuario.objects.get(id= request.POST['codigo'])
        eliminado.estado= False
        eliminado.save()
        return render(request, self.template_name, diccionario)

class MostrarUsuario(UsuarioView):
    template_name = 'Usuario/MostrarUsuario.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        mostrar= Usuario.objects.get(id= request.POST['codigo'])
        diccionario['usuario']= mostrar
        return render(request, self.template_name, diccionario)
