from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic import TemplateView

class inicio(TemplateView):
    template_name = 'inicio.html'

