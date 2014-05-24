from django.conf.urls import patterns, include, url
from .views import SolicitudesDeFaseview, VotarFase, VotarFaseConfirm
from django.contrib import admin
admin.autodiscover()

urlpatterns= patterns('',
    url(r'^$', SolicitudesDeFaseview.as_view(), name="Solicitudes_De_Fase"),
    url(r'^votarFase/$',VotarFase.as_view(), name='Votar_fase'),
    url(r'^votarFase/confirmar/$',VotarFaseConfirm.as_view(), name='Votar_fase_confirmar'),

    )