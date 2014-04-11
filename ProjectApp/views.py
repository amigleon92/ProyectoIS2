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
        buscar_user = request.POST['user']
        buscar_password = request.POST['pass']
        for i in Usuarios.objects.all():
            if i.nick == buscar_user and i.password == buscar_password:
                return render(request, 'inicio.html')
        return render(request, 'login.html')
    def get(self, request, *args, **kwargs):
        return render(request, 'inicio.html')

class RegistrarUsuario(TemplateView):
    def post(self, request, *args, **kwargs):
        return render(request, 'CrearUsuario.html')


class ListarUsuario(TemplateView):
    def post(self, request, *args, **kwargs):   #insertamos un usuario en la tabla
        new_user= request.POST['user']          #lo que nos devuelve el html en 'user'
        new_nombre= request.POST['nombre']
        new_apellido= request.POST['apellido']
        new_email= request.POST['email']
        new_cedula= request.POST['cedula']
        new_password= request.POST['pass']
        nuevo_usuario= Usuarios(nick= new_user, nombre= new_nombre, apellido= new_apellido, email= new_email, cedula= new_cedula, password= new_password) #insert into values
        nuevo_usuario.save()                    #guardamos en la base de datos
        lista= Usuarios.objects.all()
        return render(request, 'Usuario.html', {   'lista_usuarios':lista})     #enviamos al html un diccionario que tiene par 'key':lista_de_Usuarios_Existentes
    def get(self, request, *args, **kwargs):
        lista= Usuarios.objects.all()
        return render(request, 'Usuario.html', {'lista_usuarios':lista})


