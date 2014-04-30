from django.conf.urls import patterns, include, url
from .views import LoginView

from django.contrib import admin
admin.autodiscover()

urlpatterns= patterns('',
    #AUTENTICACION
    url(r'^$', LoginView.as_view(), name="login" ),
    #PROYECTO
    url(r'^proyecto/', include('Aplicaciones.Proyecto.urls')),
)
