from django.shortcuts import render
from django.shortcuts import redirect
from .models import Route, RouteInstance, NodeDestination, NodeOrigin, Perfil
from .forms import RouteForm, OriginForm, DestinationForm
from django.views import generic
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from datetime import datetime
import time    
from django.contrib.auth.models import User   

def index(request):
    
    """Función vista para la página inicio del sitio. 
        Genera datos de algunos de los objetos principales.

    Args:
        request (_type_): _description_

    Returns:
        _type_:  Renderiza la plantilla HTML index.html con los datos en la variable contexto
    """
   
    try:     

        to_send_p = Route.objects.filter( user = request.user ).filter(status= "p" )
         
        to_send_c = Route.objects.filter( user = request.user ).filter(status= "c" )
        
        user = User.objects.get(username= request.user )
        
        perfil= Perfil.objects.get(user= user)
        
        to_receive_p=Route.objects.filter( destination= perfil.nodo ).filter( status= "p" )
        
        to_receive_c=Route.objects.filter( destination= perfil.nodo ).filter( status= "c" ) 
        
        return render( request,'index.html',context={'to_send_p':to_send_p,
                                                    'to_send_c':to_send_c, 
                                                    'to_receive_p':to_receive_p,
                                                    'to_receive_c':to_receive_c,                                        
          },)    
    except:

        return render( request,'index.html',)

def update_status(request, pk):
    """
    Funcion para actualizar el estado de una ruta y agrega una instancia de su estado
    detallando fecha, hora y usuario de la modificacion

    Args:
        request (_type_): _description_
        pk (_type_): _description_

    Returns:
        _type_: Redirige al listado de rutas.
    """
 
    route= Route.objects.get(id=pk)

    if route.status == "p":
        route.status = "c"
    
    elif route.status == "c":
        route.status = "r"
    
    else:
        pass
    
    
    instance= RouteInstance()
    instance.route= route
    instance.status= route.status
    instance.instance_date=  datetime.today().strftime("%Y-%m-%d")
    instance.instance_time= time.strftime("%H:%M:%S", time.localtime())
    instance.user= request.user
    instance.save()
    route.save()
    
    
    return redirect('routes')

def route_create(request,):
    
    if request.method == "POST":
        
        form = RouteForm(request.POST)
        
        if form.is_valid():
            
            post = form.save(commit=False)
            post.user= request.user
            post.save()
       
        
        return redirect('index')    
    
    else:
        form= RouteForm()
    
        return render(request, 'route/route_create.html', {'form': form})

def origin_create(request,):
    
    if request.method == "POST":
        
        form = OriginForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
        
        
        return redirect('nodes-origin')    
    
    else:
        form= OriginForm()
    
        return render(request, 'route/nodeorigin_form.html', {'form': form})
    
def destination_create(request,):
    
    if request.method == "POST":
        
        form = DestinationForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
        
        
        return redirect('nodes-destin')    
    
    else:
        form= DestinationForm()
    
        return render(request, 'route/nodedestination_form.html', {'form': form})   

class RoutesListView(generic.ListView):
    
    model = Route
    paginate_by = 10
    
class RouteDetailView(generic.DetailView):
    
    model = Route
    
class RouteInstanceListView(generic.ListView):

    model = RouteInstance
    paginate_by = 10

class RouteInstanceDetailView(generic.DetailView):

    model = RouteInstance
    
class NodeDestinationListView(generic.ListView):
    
    model = NodeDestination
    ordering = ["id"]
    paginate_by = 10
    
class NodeOriginListView(generic.ListView):
    
    model = NodeOrigin
    ordering = ["id"]
    paginate_by = 10
    
class RouteDelete(DeleteView):
    model = Route
    success_url = reverse_lazy('routes')
    





