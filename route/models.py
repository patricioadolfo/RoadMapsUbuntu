from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
import uuid
from datetime import datetime
import time
from django.contrib.auth.models import User




class NodeOrigin(models.Model):
    """
    Modelo que representa un Origen
    """
    name = models.CharField(max_length=100)
    
    address = models.CharField(max_length=100)
    
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True)




    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular de un origen.
        """
        return reverse('origin-detail', args=[str(self.id)])
     

    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        return self.name
    
    
class NodeDestination(models.Model):
    """
    Modelo que representa un Origen
    """
    name = models.CharField(max_length=100)
    
    address = models.CharField(max_length=100)
    
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True)

    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular de un origen.
        """
        return reverse('destination-detail', args=[str(self.id)])


    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        return self.name

    
class Route(models.Model):
    
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    
    origin = models.ForeignKey(NodeOrigin, on_delete=models.SET_NULL, null= True)
   
    destination = models.ForeignKey(NodeDestination, on_delete=models.SET_NULL, null= True)
    
    description = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del envío.", null= False)
    
    preparation_date = models.DateField("Fecha de Creacion", null= True, blank=True, default= datetime.today().strftime("%Y-%m-%d"))
    
    preparation_time = models.TimeField("Hora de Creacion", null= True, blank=True, default= time.strftime("%H:%M:%S", time.localtime()))
    
    ROUTE_STATUS = (
        ('p', 'Preparado'),
        ('c', 'En camino'),
        ('e', 'Entregado'),
        ('r', 'Recibido'),
    )

    status = models.CharField("Estado", max_length=1, choices=ROUTE_STATUS, blank=True, default='p',)
    
    class Meta:
        ordering = ["-preparation_date"]

    def __str__(self):
        """ 
        String que representa al objeto Route
        """
        return '%s' %(self.id)

    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Route
        """
        return reverse('route-detail', args=[str(self.id)])
    

class RouteInstance(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único")
    
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True,)
    
    ROUTE_STATUS = (
        ('p', 'Preparado'),
        ('c', 'En camino'),
        ('e', 'Entregado'),
        ('r', 'Recibido'),
    )

    status = models.CharField("Estado", max_length=1, choices=ROUTE_STATUS, blank=True, default='p',)
    
    instance_date = models.DateField(null=True, blank=True, default= datetime.today().strftime("%Y-%m-%d"))
    
    instance_time = models.TimeField("Hora de Creacion", null= True, blank=True, default= time.strftime("%H:%M:%S", time.localtime()))
    
    
    
    class Meta:
        ordering = ["-instance_date"]
        
    
    def get_absolute_url(self):
        
        return reverse('routeinstance-detail', args=[str(self.route)])


    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return f'{self.route} ({self.route.description})'
    
    
class Perfil(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null= True,)
    
    nodo =  models.ForeignKey(NodeDestination, on_delete=models.CASCADE, null= True)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.user)
    
