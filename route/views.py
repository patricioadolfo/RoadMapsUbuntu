from django.shortcuts import render
from django.shortcuts import redirect

from .models import Route, RouteInstance, NodeDestination, NodeOrigin, Perfil, States, Urls
from .forms import RouteForm, OriginForm, DestinationForm
from django.views import generic
from django.contrib.auth.models import User

User.urls = Urls.objects.filter(state= 9)     

def index(request):
    
    """Función vista para la página inicio del sitio. 
        Genera datos de algunos de los objetos principales.

    Args:
        request (_type_): _description_

    Returns:
        _type_:  Renderiza la plantilla HTML index.html con los datos en la variable contexto
    """    
    try:  

        dict_origin = []

        dict_destin= []  
        
        perfil= Perfil.objects.filter(user= request.user )

        another_destin= NodeOrigin.objects.get( name= "Destino")
        
        for node in perfil:
    
            origin = Route.objects.exclude( origin = another_destin).filter( origin = node.nodo ).filter(status= 1 )

            dict_origin.append(origin)
        
            origin = Route.objects.exclude( origin = another_destin).filter( origin = node.nodo ).filter(status= 2 )

            dict_origin.append(origin)
            
            destin = Route.objects.exclude( destination= another_destin).filter( destination= node.nodo ).filter( status= 1 )

            dict_destin.append(destin)
            
            destin = Route.objects.exclude( destination= another_destin).filter( destination= node.nodo ).filter( status= 2 ) 

            dict_destin.append(destin)

        return render( request,'index.html', context={'to_send': dict_origin, 'to_recv': dict_destin,},)    
    
    except:

        return render( request,'index.html',)

def update_status(request, pk):
    """
    Funcion para actualiza el estado a recibido o ignorado de una ruta, y agrega una 
    instancia de su estado detallando fecha, hora y usuario de la modificacion

    Args:
        request (_type_): _description_
        pk (_type_): _description_

    Returns:
        _type_: Redirige al listado de rutas.
    """
 
    route= Route.objects.get(id=pk)

    if route.status.id ==  2:

        recv= States.objects.get(state = 3)
        
        route.status = recv

        route.save()

        instance= RouteInstance()
        
        instance.route= route
        
        instance.status = recv
        
        instance.user= request.user
        
        instance.save() 

    if route.status.id ==  1:

        recv= States.objects.get(state = 7)
        
        route.status = recv

        route.save()

        instance= RouteInstance()
        
        instance.route= route
        
        instance.status = recv
        
        instance.user= request.user
        
        instance.save()    
           
    return redirect('routes')
    
def route_create(request,):
    
    if request.method == "POST":       
        
        form = RouteForm(request.POST) 

        print(form)       

        if form.is_valid():
            
            post = form.save(commit=False)

            post.user= request.user

            post.save()
            
        return redirect('index')    
    
    else:
        
        origin_perfil= Perfil.objects.filter( user= request.user)

        another_destin= NodeOrigin.objects.get( name= "Destino")
        
        form= RouteForm()

        return render( request,'route/route_create.html', context={'another_destin': another_destin, 'origin_perfil': origin_perfil, 'form': form},) 

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

    queryset = Route.objects.all().order_by('-id')[:50]
    
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
    

    





