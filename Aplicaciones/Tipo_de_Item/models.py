
# Create your models here.
from django.db import models
from Aplicaciones.Proyecto.models import Proyecto

# Create your models here.
class Tipo_de_Item(models.Model):

    nombre= models.CharField(max_length=50, null=False)
    descripcion= models.TextField(max_length=200, null=True)
    proyecto= models.ForeignKey(Proyecto, null=True)
    #atributos= models.ManyToManyField(Atributo, related_name='AtributoBase')
    activo= models.BooleanField(default=True)
    def __unicode__(self):
        return self.nombre    #shot Me down
