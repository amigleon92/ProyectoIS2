from django.http import request
from django.views.generic import TemplateView, CreateView, ListView
from ProjectApp.models import Usuarios
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, render_to_response


class login(TemplateView):
    template_name = 'login.html'
    def get(self, request, *args, **kwargs):
        return render(request,'login.html')


class inicio(TemplateView):
    def post(self, request, *args, **kwargs):
        if 'user' in request.POST:
            buscar_user = request.POST['user']
            buscar_password = request.POST['pass']
            error= ""
            for i in Usuarios.objects.all():
                if i.nick == buscar_user:
                    if i.password == buscar_password:
                        return render(request, 'inicio.html')
                    error= "Password incorrecto"
                    return render(request, 'login.html', {'error':error})
            error= "Usuario incorrecto"
            return render(request, 'login.html', {'error': error})
        else:
            return render(request, 'inicio.html')

class RegistrarUsuario(TemplateView):
    def post(self, request, *args, **kwargs):
        return render(request, 'CrearUsuario.html')


class ListarUsuario(TemplateView):
    def post(self, request, *args, **kwargs):   #insertamos un usuario en la tabla
        if 'user' in request.POST:
            new_user= request.POST['user']          #lo que nos devuelve el html en 'user'
            new_nombre= request.POST['nombre']
            new_apellido= request.POST['apellido']
            new_email= request.POST['email']
            new_cedula= request.POST['cedula']
            new_password= request.POST['pass']
            nuevo_usuario= Usuarios(nick= new_user, nombre= new_nombre, apellido= new_apellido, email= new_email, cedula= new_cedula, password= new_password) #insert into values
            nuevo_usuario.save()                    #guardamos en la base de datos
        lista= Usuarios.objects.all()
        return render(request, 'Usuario.html', {'lista_usuarios':lista})     #enviamos al html un diccionario que tiene par 'key':lista_de_Usuarios_Existentes

class CambioEstado(TemplateView):
    def post(self, request, *args, **kwargs):
        modif_codigo= request.POST['codigo']
        modificacion= Usuarios.objects.get(id=modif_codigo)
        modificacion.estado= False
        modificacion.save()
        return render(request, 'CambioEstado.html')

class EditarUsuario(TemplateView):
    def post(self, request, *args, **kwargs):
        modif_codigo= request.POST['codigo']
        modificacion= Usuarios.objects.get(id= modif_codigo)
        return render(request, 'EditarUsuario.html', {'usuario':modificacion})

class EditarUsuarioConfirmar(TemplateView):
    def post(self, request, *args, **kwargs):
        modif_codigo= request.POST['codigo']
        modificacion= Usuarios.objects.get(id= modif_codigo)
        modificacion.nick= request.POST['user']
        modificacion.nombre= request.POST['nombre']
        modificacion.apellido= request.POST['apellido']
        modificacion.email= request.POST['email']
        modificacion.password= request.POST['pass']
        modificacion.save()
        lista= Usuarios.objects.all()
        return render(request, 'Usuario.html', {'lista_usuarios':lista})