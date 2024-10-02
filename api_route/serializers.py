from django.contrib.auth.models import User   
from rest_framework import serializers

from route import models

class RouteSerializer(serializers.ModelSerializer):
    
    origin_name = serializers.ReadOnlyField(source='origin.name')
    destination_name = serializers.ReadOnlyField(source='destination.name')
    
    
    class Meta:
        model = models.Route
        read_only_fields = ('origin_name', 'destination_name')
   
        fields = "__all__"

class instanceSerializer(serializers.ModelSerializer):
    
    route_id = serializers.ReadOnlyField(source='route.id')
    
    class Meta:
        model = models.RouteInstance
        read_only_fields = ('route_id',)
   
        fields = "__all__"
       
class OriginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.NodeOrigin
        fields = ['id', 'name','address', 'phoneNumber']
        
class DestinationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.NodeDestination
        fields = ['id', 'name','address', 'phoneNumber']
        
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        
class PerfilSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Perfil
        fields = "__all__"

class PrintJobSerializer(serializers.ModelSerializer):

    job_id = serializers.ReadOnlyField(source='job.id')
    
    printer_name = serializers.ReadOnlyField(source='printer.name')

    state_id= serializers.ReadOnlyField(source= 'state.state')
    
    class Meta:
        
        model = models.PrintJob

        read_only_fields = ('job_id', 'printer_name', 'state_id')

        fields= "__all__"