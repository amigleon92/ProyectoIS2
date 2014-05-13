from django.db import models
from Aplicaciones.Tipo_de_Item.models import Tipo_de_Item

# Create your models here.
class Atributo(models.Model):

    nombre= models.CharField(max_length=50, null=False)
    descripcion= models.TextField(max_length=200, null=True)
    tipo= models.CharField ( max_length = 20 , null=False )

#    tipo_numerico=models.IntegerField(default=0)
#    tipo_texto=models.CharField(max_length=50, null=True)
#    tipo_boolean= models.BooleanField(default=True)
#    tipo_fecha= models.DateField(null=True)

    tipodeitem= models.ForeignKey(Tipo_de_Item, null=True)
    activo= models.BooleanField(default=True)
    def __unicode__(self):
        return self.nombre    #shot Me
