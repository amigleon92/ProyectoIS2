
from django.db import models
from Aplicaciones.Fase.models import Fase
from Aplicaciones.Linea_Base.models import LineaBase
from Aplicaciones.Tipo_de_Item.models import Tipo_de_Item

# Create your models here.
class Item(models.Model):
    """
    Se crea el modelo Item

    Estan definidos en la tabla los atributos

    - nombre: Nombre de la item
    - prioridad: Prioridad del 1 al 10
    - descripcion: Una breve descripcion del item
    - tipoDeItemAsociado:En el cual se denota el tipo de item asignado
    - estado: puede encontrarse en 4 estados: Bloqueado, Revision, Desaprobado, Aprobado.
    - pkFase: el id de la Fase a la que pertenece
    - identificador: Un id para localizar las versiones anteriores de un mismo item
    """
    estados_probables= (
        ('B','Bloqueado'),
        ('R','Revision'),
        ('D','Desaprobado'),
        ('A','Aprobado'),
    )
    nombre= models.CharField(max_length=50, null=False)
    prioridad= models.PositiveIntegerField(default=0, null=False)
    descripcion= models.TextField(max_length=200, null=True)
    version=models.PositiveIntegerField(default=1, null=True)
    version_descripcion= models.CharField(max_length=80, null=True)
    estado= models.CharField ( max_length = 1 ,  choices = estados_probables, default='D' )
    tipodeItemAsociado= models.CharField(max_length=50, null=False)
    tipo_de_item= models.ForeignKey(Tipo_de_Item, related_name='fkTipodeItemI',null=True)
    fase=models.ForeignKey(Fase, related_name='fkFaseI')
    lineaBase=models.ForeignKey(LineaBase, related_name='fkLineaBaseI', null= True)
    costo= models.PositiveIntegerField(default=0, null=True)
    activo= models.BooleanField(default=True)
    identificador= models.PositiveIntegerField(default=0, null=True)

    def __unicode__(self):
        return self.nombre


