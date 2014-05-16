from django.db import models
from Aplicaciones.Fase.models import Fase

# Create your models here.
class LineaBase(models.Model):
    """
    Se crea el modelo Linea Base

    Estan definidos en la tabla los atributos

    - nombre: Nombre de la linea base
    - estado: puede encontrarse en 2 estados: Abierto y Cerrado.
    - pkFase: el id de la Fase a la que pertenece
    """
    estados_probables= (
        ('C','Cerrada'),
        ('A','Abierta'),
    )
    nombre= models.CharField(max_length=50, null=False)
    estado= models.CharField ( max_length = 1 ,  choices = estados_probables, default='A')
    fase=models.ForeignKey(Fase, related_name='fkFaseLB')
    activo= models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre