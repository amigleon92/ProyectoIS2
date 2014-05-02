from django.conf.urls import patterns, include, url
from .views import ProyectoView, EliminarProyecto, InformeProyecto, CrearProyecto, CrearProyectoConfirm, InicializarProyecto, InicializarProyectoConfirm

urlpatterns= patterns('',
    url(r'^$', ProyectoView.as_view(), name="proyecto"),
    url(r'^crear/$', CrearProyecto.as_view(), name="crear_proyecto"),
    url(r'^crear/confirmar/$', CrearProyectoConfirm.as_view(), name="confirmar_crear_proyecto"),
    url(r'^eliminar/$', EliminarProyecto.as_view(), name="eliminar_proyecto"),
    url(r'^informe/$', InformeProyecto.as_view(), name="informe_proyecto"),
    url(r'^informe/$', InformeProyecto.as_view(), name="informe_proyecto"),
    url(r'^inicializar/$', InicializarProyecto.as_view(), name="inicializar_proyecto"),
    url(r'^inicializar/confirmar/$', InicializarProyectoConfirm.as_view(), name="inicializar_proyecto_confirmar"),

    #Fases
    url(r'^fase/', include('Aplicaciones.Fase.urls')),

    #Usuarios
    url(r'^usuario/', include('Aplicaciones.Usuario.urls'))
)
