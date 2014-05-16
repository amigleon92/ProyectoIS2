from django.db import models
from Aplicaciones.Proyecto.models import Proyecto

# Create your models here.
class Fase(models.Model):
    """
    Se crea el modelo fase

    Estan definidos en la tabla los atributos

    - nombre: Nombre de la fase
    - numero de secuencia: que se autoincrementara
    - descripcion: Una breve descripcion de la fase
    - tipoDeItemAsociado:En los cuales se listara los Items asociados a las fases
    - estado: puede encontrarse en 3 estados, Iniciado, En desarrollo y finalizado
    - fechaInicio: la fecha en que se iniciara la fase
    - fechaFin: la fecha en la que se debera de dar por terminada la fase
    - pkProyecto: el id del Proyecto al que pertenece
    """
    estados_probables= (
        ('N','NoIniciado'),
        ('I','iniciado'),
        ('D','desarrollo'),
        ('F','finalizado'),
    )
    nombre= models.CharField(max_length=50, null=False)
    numeroSecuencia = models.PositiveIntegerField(default=1, null=True) #puede ser auto incremental
    descripcion= models.TextField(max_length=200, null=True)
    numero= models.PositiveIntegerField(default=0, null=True)
    tipodeItemAsociado = models.PositiveIntegerField(default=0, null=True) #esto es por que aun no exite tipos de item, deberia ser generico
    estado= models.CharField ( max_length = 1 ,  choices = estados_probables, default='N' )
    fechaInicio= models.DateField(null=True)
    fechaFin= models.DateField(null=True) #el mismo validator de fecha
    proyecto=models.ForeignKey(Proyecto, related_name='fkProyecto')
    def __unicode__(self):
        return self.nombre