from .serializers import RouteSerializer, OriginSerializer, DestinationSerializer, instanceSerializer, UserSerializer, PerfilSerializer, PrintJobSerializer
from rest_framework import permissions, viewsets
from route import models as routemodels
from .models import QueryDict
from django.contrib.auth.models import User 

class RouteSerializerViewSet(viewsets.ModelViewSet, QueryDict):

    state= None

    queryset = routemodels.Route.objects.all().order_by('-preparation_date')[:50]
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        
        if self.request.method == 'GET':
            
            query = self.request.GET.get('q', None)
            
            if query is not None:
            
                self.dict_query(query)
            
                return routemodels.Route.objects.filter(*self.q_objects)
        
            else:

                return routemodels.Route.objects.all().order_by('-preparation_date')

        else:
                
            return routemodels.Route.objects.all().order_by('-preparation_date')

class InstanceSerializerViewSet(viewsets.ModelViewSet, QueryDict):

    queryset = routemodels.RouteInstance.objects.all().order_by('route')
    serializer_class = instanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class OriginSerializerViewSet(viewsets.ModelViewSet, QueryDict):

    queryset = routemodels.NodeOrigin.objects.all().order_by('id')
    serializer_class = OriginSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class DestinationSerializerViewSet(viewsets.ModelViewSet, QueryDict):

    queryset = routemodels.NodeDestination.objects.all().order_by('name')
    serializer_class = DestinationSerializer

    permission_classes =[permissions.IsAuthenticated]
    
class UserSerializerViewSet(viewsets.ModelViewSet, QueryDict):
    
    queryset= User.objects.all()
    serializer_class= UserSerializer 
    permission_classes= [permissions.IsAuthenticated]
    
    def get_queryset(self, *args, **kwargs):
        return User.objects.filter(username =self.request.user)
    
class PerfilSerializerViewSet(viewsets.ModelViewSet, QueryDict):
    
    queryset= routemodels.Perfil.objects.all()
    serializer_class= PerfilSerializer
    permission_classes= [permissions.IsAuthenticated]
    
    def get_queryset(self):
        
        if self.request.method == 'GET':
            
            query = self.request.GET.get('q', None)
            
            if query is not None:
            
                self.dict_query(query)
            
                return routemodels.Perfil.objects.filter(*self.q_objects)
        
            else:
                return routemodels.Perfil.objects.all()

class PrintJobSerializerViewSet(viewsets.ModelViewSet, QueryDict):

    queryset= routemodels.PrintJob.objects.all()
    
    serializer_class= PrintJobSerializer
    
    permission_classes= [permissions.IsAuthenticated]
    
    def get_queryset(self):
        
        if self.request.method == 'GET':
            
            query = self.request.GET.get('q', None)
            
            if query is not None:
            
                self.dict_query(query)
            
                return routemodels.PrintJob.objects.filter(*self.q_objects)
        
            else:

                return routemodels.PrintJob.objects.all()
