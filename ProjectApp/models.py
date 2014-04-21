"""
    Django models for ProyectoIS2 project

"""
from django.db import models

class Roles(models.Model):


    nombre= models.CharField(max_length=30, unique=True)
    crear_usuario= models.BooleanField(default=False)           # - Permisos de Administracion de usuarios
    modificar_usuario= models.BooleanField(default=False)
    eliminar_usuario= models.BooleanField(default=False)
    crear_rol= models.BooleanField(default=False)               # - Permisos de Administracion de roles
    modificar_rol= models.BooleanField(default=False)
    eliminar_rol= models.BooleanField(default=False)
    crear_proyecto= models.BooleanField(default=False)          # - Permisos de Administracion de Proyectos
    iniciar_proyecto= models.BooleanField(default=False)
    finalizar_proyecto= models.BooleanField(default=False)
    eliminar_proyecto= models.BooleanField(default=False)
    crear_fase= models.BooleanField(default=False)              # - Permisos de Administracion de fases
    modificar_fase= models.BooleanField(default=False)
    cerrar_fase= models.BooleanField(default=False)
    asignar_miembro= models.BooleanField(default=False)         # - Tareas de los miembros del comite
    votar= models.BooleanField(default=False)
    consultar_solicitud= models.BooleanField(default=False)
    crear_item= models.BooleanField(default=False)              # - Permisos de Administracion de  Items
    eliminar_item= models.BooleanField(default=False)
    editar_item= models.BooleanField(default=False)
    consultar_items= models.BooleanField(default=False)
    establecer_relacion= models.BooleanField(default=False)
    eliminar_relacion= models.BooleanField(default=False)
    aprobar_item= models.BooleanField(default=False)
    revivir_item= models.BooleanField(default=False)
    revertir_item= models.BooleanField(default=False)
    consultar_relaciones= models.BooleanField(default=False)
    agregar_atributo= models.BooleanField(default=False)        # - Permisos de Administracion de atributos
    eliminar_atributo= models.BooleanField(default=False)
    completar_atributos= models.BooleanField(default=False)
    consultar_atributos= models.BooleanField(default=False)
    crear_tipodeitem= models.BooleanField(default=False)        # - Permisos de Administracion de tipos de item
    modificar_tipodeitem= models.BooleanField(default=False)
    eliminar_tipodeotem= models.BooleanField(default=False)
    crear_lineabase= models.BooleanField(default=False)         # - Permisos de Administracion de Lineas Base
    def __unicode__(self):
        return self.nombre

class Usuarios(models.Model):

    """
    Se crea el modelo Usuarios que es una base de datos definida por nosotros para manejar los usuarios que puedan
    ingresar al sistema

    Estan definidos en la tabla los atributos

    - nick: Por el cual se va a loguear al sistema
    - nombre: Nombre del usuario
    - apellido: Apellido del usuario
    - password: Contrasenha para el logueo
    - cedula: Cedula de identidad del usuario
    - email: Direccion de correo electronico del usuario
    - estado: - ACTIVO: puede ingresar al sistema
              - INACTIVO: usuario eliminado
    """
    nick= models.CharField(max_length=15, unique=False)
    nombre= models.CharField(max_length=50, null=False)
    apellido= models.CharField(max_length=50, null=False)
    password= models.CharField(max_length=10)
    cedula= models.PositiveIntegerField(default=0)
    email= models.CharField(max_length=20, null=False)
    estado= models.BooleanField(default=True)
    permiso= models.ManyToManyField(Roles)                      #El rol asociado al usuario
    def __unicode__(self):
        return self.nombre

class Proyecto(models.Model):
    """
    Se crea el modelo Proyecto

    Estan definidos en la tabla los atributos

    - Codigo: Que es el PK de la tabla y se autoCompletara
    - nombre: Nombre del proyecto
    - descripcion: Una breve descripcion
    - usuario: una lista de usuarios asociados al proyecto
    - presupuesto: el presupuesto que se pasa por el proyecto
    - estado: puede encontrarse en 3 estados, Iniciado, En desarrollo y finalizado
    - costoTemporal: el costo en dias del Proyecto
    - costoMonetario: El costo en moneda local de la realizacion
    - fechaInicio: la fecha en que se iniciara el Proyecto
    - fecchaFin: la fache en la que se debera de dar por terminado el proyecto
    """
    estados_probables= (
        ('I','iniciado'),
        ('N','noIniciado'),
        ('F','finalizado'),
    )
    codigo= models.AutoField(primary_key= True)
    nombre= models.CharField(max_length=50, null=False, unique=True )
    descripcion= models.TextField(max_length=200, null=True)
    lider=models.ForeignKey(Usuarios,related_name='Lider')
    usuarios= models.ManyToManyField(Usuarios, related_name='UsuarioBase')
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

class Fase(models.Model):
    """
    Se crea el modelo fase

    Estan definidos en la tabla los atributos

    - nombre: Nombre de la fase
    - numero de secuencia: que se autoincrementara
    - descripcion: Una breve descripcion de la fase
    - numero:
    - tipoDeItemAsociado:En los cuales se listara los Items asociados a las fases
    - estado: puede encontrarse en 3 estados, Iniciado, En desarrollo y finalizado
    - fechaInicio: la fecha en que se iniciara la fase
    - fechaFin: la fecha en la que se debera de dar por terminada la fase
    """
    estados_probables= (
        ('I','iniciado'),
        ('D','desarrollo'),
        ('F','finalizado'),
    )
    nombre= models.CharField(max_length=50, null=False)
    numeroSecuencia = models.PositiveIntegerField(default=1) #puede ser auto incremental
    descripcion= models.TextField(max_length=200)
    numero= models.PositiveIntegerField(default=0)
    tipodeItemAsociado = models.PositiveIntegerField(default=0) #esto es por que aun no exite tipos de item, deberia ser generico
    estado= models.CharField ( max_length = 1 ,  choices = estados_probables )
    fechaInicio= models.DateField()
    fechaFin= models.DateField() #el mismo validator de fecha
    def __unicode__(self):
        return self.nombre