from django.db import models
from Aplicaciones.Item.models import Item

# Create your models here.
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
        ('A/S', 'RelacionAntecesorSucesor'),
        ('P/H', 'RelacionPadreHijo')
    )
    nombre= models.CharField(max_length=50)
    item1= models.ForeignKey(Item, related_name='fkItem1')
    item2= models.ForeignKey(Item, related_name='fkItem2')
    tipo= models.CharField(max_length=3, choices=relaciones_probables)
    activo= models.BooleanField(default=True)
    def __unicode__(self):
        return self.nombre
