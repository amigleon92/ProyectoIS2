
from django.db import models
from Aplicaciones.Fase.models import Fase

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
    tipodeItemAsociado = models.CharField(max_length=50, null=False)
    estado= models.CharField ( max_length = 1 ,  choices = estados_probables, default='D' )
    fase=models.ForeignKey(Fase, related_name='fkFaseI')
    costo= models.PositiveIntegerField(default=0, null=True)
    activo= models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre