
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

class Relacion(models.Model):
    """
    Se crea el modelo Relacion (Las relaciones van a estar definidas de la forma item1 -> item2)

    Estan definidos los atributos

    - nombre= Nombre de la relacion
    - item1= FK al primer item de la relacion
    - item2= FK del segundo item de la relacion
    - tipo= Puede tener 2 tipos: RelacionAntecesorSucesor, RelacionPadreHijo
    """
    relaciones_probables= (
        ('A', 'RelacionAntecesorSucesor'),
        ('P', 'RelacionPadreHijo')
    )
    nombre= models.CharField(max_length=50)
    item1= models.ForeignKey(Item, related_name='fkItem1')
    item2= models.ForeignKey(Item, related_name='fkItem2')
    tipo= models.CharField(max_length=1, choices=relaciones_probables)
    activo= models.BooleanField(default=True)
    def __unicode__(self):
        return self.nombre

