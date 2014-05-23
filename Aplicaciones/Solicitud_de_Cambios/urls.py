from django.conf.urls import patterns, include, url
from .views import SolicitudesDeFaseview
from django.contrib import admin
admin.autodiscover()

urlpatterns= patterns('',
    url(r'^$', SolicitudesDeFaseview.as_view(), name="Solicitudes_De_Fase"),

    )