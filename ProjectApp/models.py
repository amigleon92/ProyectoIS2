"""
    Django models for ProyectoIS2 project

    Se crea el modelo Usuarios que es una base de datos definida por nosotros para manejar los usuarios que puedan
    ingresar al sistema

    Estan definidos en la tabla los atributos
    nick: Por el cual se va a loguear al sistema
    nombre: Nombre del usuario
    apellido: Apellido del usuario
    password: Contrasenha para el logueo
    cedula: Cedula de identidad del usuario
    email: Direccion de correo electronico del usuario
    estado: ACTIVO: puede ingresar al sistema
            INACTIVO: usuario eliminado

"""
from django.db import models

class Roles(models.Model):
    nombre= models.CharField(max_length=30, unique=True)
    crear_usuario= models.BooleanField(default=False)           #Permisos de Administracion de usuarios
    modidificar_usuario= models.BooleanField(default=False)
    eliminar_usuario= models.BooleanField(default=False)
    crear_rol= models.BooleanField(default=False)               #Permisos de Administracion de roles
    modificar_rol= models.BooleanField(default=False)
    eliminar_rol= models.BooleanField(default=False)
    crear_proyecto= models.BooleanField(default=False)          #Permisos de Administracion de Proyectos
    iniciar_proyecto= models.BooleanField(default=False)
    finalizar_proyecto= models.BooleanField(default=False)
    crear_fase= models.BooleanField(default=False)              #Permisos de Administracion de fases
    modificar_fase= models.BooleanField(default=False)
    cerrar_fase= models.BooleanField(default=False)
    asignar_miembro= models.BooleanField(default=False)         #Tareas de los miembros del comite
    votar= models.BooleanField(default=False)
    consultar_solicitud= models.BooleanField(default=False)
    crear_item= models.BooleanField(default=False)              #Permisos de Administracion de  Items
    eliminar_item= models.BooleanField(default=False)
    editar_item= models.BooleanField(default=False)
    consultar_items= models.BooleanField(default=False)
    establecer_relacion= models.BooleanField(default=False)
    eliminar_relacion= models.BooleanField(default=False)
    aprobar_item= models.BooleanField(default=False)
    revivir_item= models.BooleanField(default=False)
    revertir_item= models.BooleanField(default=False)
    consultar_relaciones= models.BooleanField(default=False)
    agregar_atributo= models.BooleanField(default=False)        #Permisos de Administracion de atributos
    eliminar_atributo= models.BooleanField(default=False)
    completar_atributos= models.BooleanField(default=False)
    consultar_atributos= models.BooleanField(default=False)
    crear_tipodeitem= models.BooleanField(default=False)        #Permisos de Administracion de tipos de item
    modificar_tipodeitem= models.BooleanField(default=False)
    eliminar_tipodeotem= models.BooleanField(default=False)
    crear_lineabase= models.BooleanField(default=False)         #Permisos de Administracion de Lineas Base

class Usuarios(models.Model):
    nick= models.CharField(max_length=15, unique=False)
    nombre= models.CharField(max_length=50, null=False)
    apellido= models.CharField(max_length=50, null=False)
    password= models.CharField(max_length=10)
    cedula= models.PositiveIntegerField(default=0)
    email= models.CharField(max_length=20, null=False)
    estado= models.BooleanField(default=True)
    permiso= models.ManyToManyField(Roles)                      #El rol asociado al usuario
    def __unicode__(self):
        return self.nombre

class Proyecto(models.Model):
    pass


