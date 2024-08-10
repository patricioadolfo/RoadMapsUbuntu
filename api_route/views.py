from .serializers import RouteSerializer, OriginSerializer, DestinationSerializer, instanceSerializer, UserSerializer, PerfilSerializer
from rest_framework import permissions, viewsets
from route import models
from django.contrib.auth.models import User 
from django.db.models import Q
import json
#from myapp.models import User
#user_dict = {'name': 'Charlie', 'age': 40}
#q_objects = [Q(**{k: v}) for k, v in user_dict.items()]
#queryset = User.objects.filter(*q_objects)

class QueryDict():

    def dict_query(self, dict):
        
        d= json.loads(dict)
        
        self.q_objects = [Q(**{k: v}) for k, v in d.items()]

class RouteSerializerViewSet(viewsets.ModelViewSet, QueryDict):

    queryset = models.Route.objects.all().order_by('-preparation_date')
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        
        if self.request.method == 'GET':
            
            query = self.request.GET.get('q', None)
            
            if query is not None:
            
                self.dict_query(query)
            
                return models.Route.objects.filter(*self.q_objects)
        
            else:
                return models.Route.objects.all().order_by('-preparation_date')
        else:
            return models.Route.objects.all().order_by('-preparation_date')

class InstanceSerializerViewSet(viewsets.ModelViewSet, QueryDict):

    queryset = models.RouteInstance.objects.all().order_by('route')
    serializer_class = instanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class OriginSerializerViewSet(viewsets.ModelViewSet, QueryDict):

    queryset = models.NodeOrigin.objects.all().order_by('id')
    serializer_class = OriginSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class DestinationSerializerViewSet(viewsets.ModelViewSet, QueryDict):

    queryset = models.NodeDestination.objects.all().order_by('name')
    serializer_class = DestinationSerializer

    permission_classes =[permissions.IsAuthenticated]
    
class UserSerializerViewSet(viewsets.ModelViewSet, QueryDict):
    
    queryset= User.objects.all()
    serializer_class= UserSerializer 
    permission_classes= [permissions.IsAuthenticated]
    
    def get_queryset(self, *args, **kwargs):
        return User.objects.filter(username =self.request.user)
    
class PerfilSerializerViewSet(viewsets.ModelViewSet, QueryDict):
    
    queryset= models.Perfil.objects.all()
    serializer_class= PerfilSerializer
    permission_classes= [permissions.IsAuthenticated]
    
    def get_queryset(self):
        
        if self.request.method == 'GET':
            
            query = self.request.GET.get('q', None)
            
            if query is not None:
            
                self.dict_query(query)
            
                return models.Perfil.objects.filter(*self.q_objects)
        
            else:
                return models.Perfil.objects.all()

        
   
