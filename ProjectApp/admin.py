from django.contrib import admin

# Register your models here.

from ProjectApp.models import Usuarios, Roles
admin.site.register(Usuarios)
admin.site.register(Roles)
