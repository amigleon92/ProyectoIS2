from django.views.generic import TemplateView, CreateView, ListView
from ProjectApp.models import Usuarios
from django.core.urlresolvers import reverse_lazy

class login(TemplateView):
    template_name = 'login.html'

class inicio(TemplateView):
    template_name = "inicio.html"

class RegistrarUsuario(CreateView):
    template_name = "CrearUsuario.html"
    model = Usuarios
    success_url = reverse_lazy('listar_usuario')

class ListarUsuario(ListView):
    template_name = 'Usuario.html'
    model = Usuarios