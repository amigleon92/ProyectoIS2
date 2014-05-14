
# Create your models here.
from django.db import models
from Aplicaciones.Proyecto.models import Proyecto

# Create your models here.
class Tipo_de_Item(models.Model):
    """
    Se crea el modelo tipo de Item

    Estan definidos en la tabla los atributos

    - nombre: Nombre del tipo de atributo
    - descripcion: una breve descripcion del tipo de item.
    - cantidad_de_item: numerico de la cantidad de item
    - proyecto: proyecto al que pertenece
    - activo: estado logico del tipo de item
    """
    nombre= models.CharField(max_length=50, null=False)
    descripcion= models.TextField(max_length=200, null=True)

    cantidad_de_item=models.PositiveIntegerField(default=0, null=True)
    proyecto= models.ForeignKey(Proyecto, null=True)
    activo= models.BooleanField(default=True)
    def __unicode__(self):
        return self.nombre    #shot Me down
