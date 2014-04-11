from django.http import request
from django.views.generic import TemplateView, CreateView, ListView
from ProjectApp.models import Usuarios
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, render_to_response


class login(TemplateView):
    template_name = 'login.html'


class inicio(TemplateView):
    def post(self, request, *args, **kwargs):
        buscar_user = request.POST['user']
        buscar_password = request.POST['pass']
        for i in Usuarios.objects.all():
            if i.nick == buscar_user and i.password == buscar_password:
                return render(request, 'inicio.html')
        return render(request, 'login.html')

class RegistrarUsuario(CreateView):
    template_name = 'CrearUsuario.html'
    model = Usuarios
    success_url = reverse_lazy('listar_usuario')


class ListarUsuario(TemplateView):
    def post(self, request, *args, **kwargs):

        return render(request, 'Usuario.html')
