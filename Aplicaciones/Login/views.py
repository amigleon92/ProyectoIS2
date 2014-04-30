from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import request

# Create your views here.

class LoginView(TemplateView):
    template_name = 'Login/Login.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
