from django.db import models
from Aplicaciones.Tipo_de_Item.models import Tipo_de_Item

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
    tipo= models.CharField(max_length=50, null=False)           #apunta al tipo de de atributo

    tipo_numerico=models.IntegerField(default=0)
    tipo_texto=models.CharField(max_length=50, null=True)
    tipo_boolean= models.BooleanField(default=True)
    tipo_fecha= models.DateField(null=True)

    tipodeitem= models.ForeignKey(Tipo_de_Item, null=True)      #apunta al tipo de item al que pertenece
    activo= models.BooleanField(default=True)
    def __unicode__(self):
        return self.nombre    #shot Me
