from django.db import models
from Aplicaciones.Item.models import Item

# Create your models here.
class Atributo(models.Model):
    """
    Se crea el modelo Atributo

    Estan definidos en la tabla los atributos

    - nombre: Nombre del atributo
    - descripcion: Una breve descripcion del atributo
    - tipo:el cual apunta al tipo de atributo
    - tipo_numerico:
    - tipo_texto:
    - tipo_boolean:
    - tipo_fecha:
    - tipodeitem: el cual apunta al tipo de item al que pertenece
    - activo: estado logico del atributo
    """
    nombre= models.CharField(max_length=50, null=False)
    descripcion= models.TextField(max_length=200, null=True)
    tipo_de_atributo_nombre= models.CharField(max_length=50, null=False)           #nombre del tipo de atributo
    tipo_de_atributo_tipo=models.CharField(max_length=1, null=True)                 #tipo del tipo de atributo

    tipo_numerico=models.IntegerField(null=True)
    tipo_texto=models.CharField(max_length=50, null=True)
    tipo_boolean= models.NullBooleanField(null=True)
    tipo_fecha= models.DateField(null=True)

    item= models.ForeignKey(Item, null=True)      #apunta al item al que pertenece
    activo= models.BooleanField(default=True)
    def __unicode__(self):
        return self.nombre    #shot Me
