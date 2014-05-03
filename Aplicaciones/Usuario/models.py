from django.db import models
#from Aplicaciones.Rol.models import Rol

# Create your models here.
class Usuario(models.Model):

    """
    Se crea el modelo Usuarios que es una base de datos definida por nosotros para manejar los usuarios que puedan
    ingresar al sistema

    Estan definidos en la tabla los atributos

    - nick: Por el cual se va a loguear al sistema
    - nombre: Nombre del usuario
    - apellido: Apellido del usuario
    - password: Contrasenha para el logueo
    - cedula: Cedula de identidad del usuario
    - email: Direccion de correo electronico del usuario
    - estado: - ACTIVO: puede ingresar al sistema
              - INACTIVO: usuario eliminado
    - permiso: roles que posee un usuario
    """
    nick= models.CharField(max_length=15, unique=True)
    nombre= models.CharField(max_length=50, null=True)
    apellido= models.CharField(max_length=50, null=True)
    password= models.CharField(max_length=10)
    cedula= models.PositiveIntegerField(default=0)
    email= models.CharField(max_length=20, null=True)
    estado= models.BooleanField(default=True)
    def __unicode__(self):
        return self.nombre
