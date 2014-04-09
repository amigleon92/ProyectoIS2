from django.views.generic import TemplateView, CreateView
from ProjectApp.models import Usuarios

class login(TemplateView):
    template_name = 'login.html'

class RegistrarUsuario(CreateView):
    template_name = "CrearUsuario.html"
    model = Usuarios

