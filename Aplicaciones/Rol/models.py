from django.db import models

# Create your models here.
class Rol(models.Model):
    """
    Se crea el modelo de Rol en el cual tenemos booleans
    """
    nombre= models.CharField(max_length=30, unique=True)
    crear_usuario= models.BooleanField(default=False)           # - Permisos de Administracion de usuarios
    modificar_usuario= models.BooleanField(default=False)
    eliminar_usuario= models.BooleanField(default=False)
    crear_rol= models.BooleanField(default=False)               # - Permisos de Administracion de roles
    modificar_rol= models.BooleanField(default=False)
    eliminar_rol= models.BooleanField(default=False)
    crear_proyecto= models.BooleanField(default=False)          # - Permisos de Administracion de Proyectos
    iniciar_proyecto= models.BooleanField(default=False)
    finalizar_proyecto= models.BooleanField(default=False)
    eliminar_proyecto= models.BooleanField(default=False)
    crear_fase= models.BooleanField(default=False)              # - Permisos de Administracion de fases
    modificar_fase= models.BooleanField(default=False)
    cerrar_fase= models.BooleanField(default=False)
    asignar_miembro= models.BooleanField(default=False)         # - Tareas de los miembros del comite
    votar= models.BooleanField(default=False)
    consultar_solicitud= models.BooleanField(default=False)
    crear_item= models.BooleanField(default=False)              # - Permisos de Administracion de  Items
    eliminar_item= models.BooleanField(default=False)
    editar_item= models.BooleanField(default=False)
    consultar_items= models.BooleanField(default=False)
    establecer_relacion= models.BooleanField(default=False)
    eliminar_relacion= models.BooleanField(default=False)
    aprobar_item= models.BooleanField(default=False)
    revivir_item= models.BooleanField(default=False)
    revertir_item= models.BooleanField(default=False)
    consultar_relaciones= models.BooleanField(default=False)
    agregar_atributo= models.BooleanField(default=False)        # - Permisos de Administracion de atributos
    eliminar_atributo= models.BooleanField(default=False)
    completar_atributos= models.BooleanField(default=False)
    consultar_atributos= models.BooleanField(default=False)
    crear_tipodeitem= models.BooleanField(default=False)        # - Permisos de Administracion de tipos de item
    modificar_tipodeitem= models.BooleanField(default=False)
    eliminar_tipodeotem= models.BooleanField(default=False)
    crear_lineabase= models.BooleanField(default=False)         # - Permisos de Administracion de Lineas Base
    def __unicode__(self):
        return self.nombre
