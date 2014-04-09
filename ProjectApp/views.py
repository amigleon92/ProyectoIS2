from django.views.generic import TemplateView, CreateView
from ProjectApp.models import Usuarios

class inicio(TemplateView):
    template_name = 'inicio.html'

class RegistrarUsuario(CreateView):
    template_name = "CrearUsuario.html"
    model = Usuarios

