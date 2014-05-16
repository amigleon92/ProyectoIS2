from django.conf.urls import patterns, include, url
from .views import RolView, CrearRol, CrearRolConfirm, EditarRol, EditarRolConfirmar, EliminarRol, ConsultarRol, AsignarRol, AsignarRolConfirm, DesasignarRol
from .views import AsignarMiembroComite, AsignarMiembroComiteConfirm

urlpatterns= patterns('',
    url(r'^$', RolView.as_view(), name='rol'),
    url(r'^crear/$', CrearRol.as_view(), name='crear_rol'),
    url(r'^crear/confirmar/$', CrearRolConfirm.as_view(), name='crear_rol_confirmar'),
    url(r'^editar/$', EditarRol.as_view(), name='editar_rol'),
    url(r'^editar/confirmar/$', EditarRolConfirmar.as_view(), name='editar_rol_confirmar'),
    url(r'^eliminar/$', EliminarRol.as_view(), name='eliminar_rol'),
    url(r'^consultar_usuarios/$', ConsultarRol.as_view(), name='consultar_rol'),
    url(r'^desasignar/$', DesasignarRol.as_view(), name='desasignar_rol'),
    url(r'^asignar/$', AsignarRol.as_view(), name='asignar_rol'),
    url(r'^asignar/confirmar/$', AsignarRolConfirm.as_view(), name='asignar_rol_confirmar'),
    url(r'^asignar_miembro_comite/$', AsignarMiembroComite.as_view(), name='asignar_miembro_comite'),
    url(r'^asignar_miembro_comite/confirmar/$', AsignarMiembroComiteConfirm.as_view(), name='asignar_miembro_comite_confirmar'),
)
