from django.db import models
from Aplicaciones.Usuario.models import Usuario

# Create your models here.
class Proyecto(models.Model):
    """
    Se crea el modelo Proyecto

    Estan definidos en la tabla los atributos

    - nombre: Nombre del proyecto
    - descripcion: Una breve descripcion
    - lider: el Lider del Proyecto
    - miembros: una lista de usuarios asociados al proyecto
    - presupuesto: el presupuesto que se pasa por el proyecto
    - estado: puede encontrarse en 3 estados, Iniciado, En desarrollo y finalizado
    - costoTemporal: el costo en dias del Proyecto
    - costoMonetario: El costo en moneda local de la realizacion
    - fechaInicio: la fecha en que se iniciara el Proyecto
    - fechaFin: la fecha en la que se debera de dar por terminado el proyecto
    - activo: campo para la eliminacion logica
    - numeroFases: La cantidad de fase del Proyecto
    """
    estados_probables= (
        ('I','iniciado'),
        ('N','noIniciado'),
        ('F','finalizado'),
    )
    nombre= models.CharField(max_length=50, null=False, unique=True )
    descripcion= models.TextField(max_length=200, null=True)
    miembros= models.ManyToManyField(Usuario, related_name='UsuarioBase')
    presupuesto= models.PositiveIntegerField(null=True) #decimales positivos nada mas
    estado= models.CharField ( max_length = 1 ,choices = estados_probables,  default='N' )
    costoTemporal= models.PositiveIntegerField(default=0, null=True)
    costoMonetario= models.PositiveIntegerField(null=True) #decimales positivos nada mas
    fechaInicio= models.DateField(null=True)
    fechaFin= models.DateField(null=True)            #debe de existir un validator que verifique que la fecha no este antes que el inicio
    activo= models.BooleanField(default=True)
    numeroFase=models.PositiveIntegerField(default=1)
    def __unicode__(self):
        return self.nombre
