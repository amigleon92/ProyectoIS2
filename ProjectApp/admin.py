from django.contrib import admin

# Register your models here.

from ProjectApp.models import Usuarios, Roles, Proyecto, Fase
admin.site.register(Usuarios)
admin.site.register(Roles)
admin.site.register(Proyecto) #para que muestre en la administracion el modelo proyecto
admin.site.register(Fase)