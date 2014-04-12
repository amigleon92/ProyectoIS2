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

class Usuarios(models.Model):
    nick= models.CharField(max_length=15)
    nombre= models.CharField(max_length=50)
    apellido= models.CharField(max_length=50)
    password= models.CharField(max_length=10)
    cedula= models.PositiveIntegerField()
    email= models.CharField(max_length=20)
    estado= models.BooleanField(default=True)

