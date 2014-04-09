from django.db import models

class Usuarios(models.Model):
    nick= models.CharField(max_length=15)
    nombre= models.CharField(max_length=50)
    apellido= models.CharField(max_length=50)
    password= models.CharField(max_length=10)
    cedula= models.PositiveIntegerField()
    email= models.CharField(max_length=20)
    def __unicode__(self):
        return self.nick
