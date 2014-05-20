from django.db import models
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.Proyecto.models import Proyecto

# Create your models here.
class Rol(models.Model):
    nombre= models.CharField(max_length=50)
    usuario= models.ForeignKey(Usuario)                             # - El usuario que tiene dicho rol
    proyecto= models.ForeignKey(Proyecto, null=True)                # - A que proyecto se asocia dicho rol
    #crear_usuario= models.BooleanField(default=False)  admin       # - Permisos de Administracion de usuarios
    #modificar_usuario= models.BooleanField(default=False) admin
    #eliminar_usuario= models.BooleanField(default=False) admin
    #crear_rol= models.BooleanField(default=False) lider            # - Permisos de Administracion de roles
    #modificar_rol= models.BooleanField(default=False) lider
    #eliminar_rol= models.BooleanField(default=False) lider
    #crear_proyecto= models.BooleanField(default=False) admin       # - Permisos de Administracion de Proyectos
    #iniciar_proyecto= models.BooleanField(default=False) lider
    #finalizar_proyecto= models.BooleanField(default=False) lider
    #eliminar_proyecto= models.BooleanField(default=False) lider
    #crear_fase= models.BooleanField(default=False) lider           # - Permisos de Administracion de fases
    #modificar_fase= models.BooleanField(default=False) lider
    #cerrar_fase= models.BooleanField(default=False) lider
    #asignar_miembro= models.BooleanField(default=False) lider      # - Tareas de los miembros del comite
    #votar= models.BooleanField(default=False)
    #consultar_solicitud= models.BooleanField(default=False)
    crear_item= models.BooleanField(default=False)                  # - Permisos de Administracion de  Items
    eliminar_item= models.BooleanField(default=False)
    editar_item= models.BooleanField(default=False)
    consultar_items= models.BooleanField(default=False)
    establecer_relacion= models.BooleanField(default=False)
    eliminar_relacion= models.BooleanField(default=False)
    aprobar_item= models.BooleanField(default=False)
    revivir_item= models.BooleanField(default=False)
    revertir_item= models.BooleanField(default=False)
    reversionar_item= models.BooleanField(default=False)
    consultar_relaciones= models.BooleanField(default=False)
    agregar_atributo= models.BooleanField(default=False)            # - Permisos de Administracion de atributos
    eliminar_atributo= models.BooleanField(default=False)
    completar_atributos= models.BooleanField(default=False)
    consultar_atributos= models.BooleanField(default=False)
    crear_tipodeitem= models.BooleanField(default=False)            # - Permisos de Administracion de tipos de item
    modificar_tipodeitem= models.BooleanField(default=False)
    eliminar_tipodeitem= models.BooleanField(default=False)
    crear_tipodeatributo= models.BooleanField(default=False)            # - Permisos de Administracion de tipos de atributos
    eliminar_tipodeatributo= models.BooleanField(default=False)
    crear_lineabase= models.BooleanField(default=False)             # - Permisos de Administracion de Lineas Base


    activo= models.BooleanField(default=True)
    def __unicode__(self):
        return self.nombre
