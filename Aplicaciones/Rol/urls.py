from django.conf.urls import patterns, include, url
from .views import RolView, CrearRol, CrearRolConfirm, EditarRol, EditarRolConfirmar, EliminarRol

urlpatterns= patterns('',
    url(r'^$', RolView.as_view(), name='rol'),
    url(r'^crear/$', CrearRol.as_view(), name='crear_rol'),
    url(r'^crear/confirmar/$', CrearRolConfirm.as_view(), name='crear_rol_confirmar'),
    url(r'^editar/$', EditarRol.as_view(), name='editar_rol'),
    url(r'^editar/confirmar/$', EditarRolConfirmar.as_view(), name='editar_rol_confirmar'),
    url(r'^eliminar/', EliminarRol.as_view(), name='eliminar_rol'),
)
