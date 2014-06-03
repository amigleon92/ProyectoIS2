from django.conf.urls import patterns, include, url
from .views import SolicitudesDeFaseview, VotarFase, VotarFaseConfirm, SolicitudesDeProyectoView, VotarProyecto,VotarProyectoConfirm
from django.contrib import admin
admin.autodiscover()

urlpatterns= patterns('',
    url(r'^SolicitudMiembro/$', SolicitudesDeProyectoView.as_view(), name="Solicitudes_De_Proyecto"),
    url(r'^SolicitudMiembro/votarProyecto/$', VotarProyecto.as_view(), name="Votar_Proyecto"),
    url(r'^SolicitudMiembro/votarProyecto/confirmar/$', VotarProyectoConfirm.as_view(), name="Votar_Proyecto_confirmar"),
    url(r'^$', SolicitudesDeFaseview.as_view(), name="Solicitudes_De_Fase"),
    url(r'^votarFase/$',VotarFase.as_view(), name='Votar_fase'),
    url(r'^votarFase/confirmar/$',VotarFaseConfirm.as_view(), name='Votar_fase_confirmar'),

    )