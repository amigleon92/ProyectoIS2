from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from ProjectApp.views import inicio, RegistrarUsuario

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ProyectoIS2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', inicio.as_view() ),
    url(r'^usuario/crearusuario$', RegistrarUsuario.as_view(), name= 'registrar_usuario'),
)
