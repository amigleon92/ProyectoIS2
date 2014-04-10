from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from ProjectApp.views import login, RegistrarUsuario, inicio, ListarUsuario


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ProyectoIS2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login.as_view() ),
    url(r'^inicio$', inicio.as_view() ),
    url(r'^inicio/usuario/crear$', RegistrarUsuario.as_view(), name= 'registrar_usuario'),
    url(r'^inicio/usuario$', ListarUsuario.as_view(), name= 'listar_usuario'),
)
