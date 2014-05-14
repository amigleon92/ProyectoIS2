from django.db import models
from Aplicaciones.Proyecto.models import Proyecto

# Create your models here.
class Tipo_de_Atributo(models.Model):
    """
    Se crea el modelo tipo de Atributo

    Estan definidos en la tabla los atributos

    - nombre: Nombre del tipo de atributo
    - tipo: eleccion de los tipos de atributos que pueden ser Numerico, Boolean, texto, fecha
    - proyecto: proyecto al que pertenece
    - activo: estado logico del tipo de atributo
    """
    tipos_probables= (
        ('N','Numerico'),
        ('B','Buleano'),
        ('T','Texto'),
        ('F','Fecha'),
    )
    nombre= models.CharField(max_length=50, null=False)
    tipo= models.CharField ( max_length = 1 ,  choices = tipos_probables, default='N' )

#    tipo_numerico=models.IntegerField(default=0)
#    tipo_texto=models.CharField(max_length=50, null=False)
#    tipo_boolean= models.BooleanField(default=True)
#    tipo_fecha= models.DateField(null=True)

    proyecto= models.ForeignKey(Proyecto, null=True)
    activo= models.BooleanField(default=True)
    def __unicode__(self):
        return self.nombre    #shot Me
