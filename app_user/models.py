import requests
from datetime import datetime
import time
from threading import Thread
from kivy.clock import Clock

def deco(funcion):
    
    def envolvente(*args):
                
        thread = Thread(name= str(funcion),target=funcion, args=args)

        thread.start()

        return thread
        
    return envolvente

class Route:
    
    def __init__(self,):    
        
        pass
        
    def get_url(self, id= ''):

        r= self.client.get( self.url + id )

        if r.status_code == 200:
            
            return r.json()
        
        else:
            return False
        
    def patch_url(self, id, payload):
        
        self.url= self.url +  id + '/'
        
        self.client.get(self.url)   

        if 'csrftoken' in self.client.cookies:
            
            csrftoken = self.client.cookies['csrftoken']
        
            patch= self.client.patch(self.url, data= payload, headers={'X-CSRFTOKEN': csrftoken})
          
            return patch.status_code
        
    def post_url(self, payload):
        
        self.client.get(self.url) 
        
        if 'csrftoken' in self.client.cookies:

            csrftoken = self.client.cookies['csrftoken']
            
            payload['csrfmiddlewaretoken']= csrftoken
            
            payload['next']= ''
            
            post= self.client.post(self.url, data= payload, headers=dict(Referer= self.url))
            
            return post

class User(Route):
    
    def __init__(self,):
        
        self.id_user= {}
        
        self.dict= {}

        self._dict= {}

        self.time_preload= 60

        self.stop= False

        self.clock= Clock

    def view_nodes(self, url):
        
        self.url= url
        
        get= self.get_url('')
        
        return get['results']
    
    def log(self, url, user, passwd):
        
        url= 'http://' + url 
        
        self.url=''
                
        self.url_route= url + '/api/api-route/'

        self.url_instance= url + '/api/api-instance/'

        self.url_id_user= url + '/api/api-user/'

        self.url_origin= url + '/api/api-origin/'
        
        self.url_destin= url + '/api/api-destination/'    
   
        self.url_login= url + '/api-auth/login/'
        
        self.url_logout= url + '/api-auth/logout/'
        
        self.url_perfil= url + '/api/api-perfil/'

        self.url_print_job= url + '/api/api-printjob/'
        
        self.client = requests.session()
        
        self.client.get(self.url_login) 
        
        if 'csrftoken' in self.client.cookies:

            csrftoken = self.client.cookies['csrftoken']
            
            login_data = dict(username= user, password= passwd, csrfmiddlewaretoken=csrftoken, next='/api/api-user/')
            
            id = self.client.post(self.url_login, data=login_data, headers=dict(Referer= self.url_login))
        
            self.id_user= id.json()['results'][0]         
            
            self.url= self.url_perfil

            perfil = self.get_url('?q='+ str({"user": self.id_user['id']}).replace("'",'"').replace(' ',''))
            
            self.perfil= perfil['results'][0]['nodo']

    def logOut(self,):

        self.id_user= {}

        self.dict= {}

        self.stop = True
        
        if 'csrftoken' in self.client.cookies:

            csrftoken = self.client.cookies['csrftoken']
       
            self.client.post(self.url_logout, data=dict(csrfmiddlewaretoken=csrftoken, next=''), headers=dict(Referer= self.url_logout))
            
    def receive(self, id_route):
        
        self.url= self.url_route
     
        payload= {"status": 3}
    
        patch= self.patch_url(id_route, payload)
        
        if patch == 200:

            payload={
                "route_id": id_route,
                "status": 3,
                "instance_date":  datetime.today().strftime("%Y-%m-%d"),
                "instance_time": time.strftime("%H:%M:%S", time.localtime()),
                "user": self.id_user['id'],
                "route": id_route
            }
            
            self.url= self.url_instance

            self.post_url(payload)        

            return True
        
        else: 
            
            return False
        


    def view_road(self, query):
        
        self.url= self.url_route
        
        route= self.get_url(query)
        
        return route
               
    def route_create(self, detail, branch):
        
        self.url= self.url_route
        
        payload= { 
                    "description": detail,
                    "preparation_date": datetime.today().strftime("%Y-%m-%d"),
                    "preparation_time":  time.strftime("%H:%M:%S", time.localtime()),
                    "status": 1,
                    "user": self.id_user['id'],
                    "origin": self.perfil,
                    "destination": branch['id']
                  }        
        
        post= self.post_url(payload)

        if post.status_code == 201:

            id = post.json()['id']

            try:

                self.url= self.url_print_job

                payload= {
                    'job': id,
                    'printer': self.id_user['id']
                }
                
                self.post_url(payload)

            except:

                pass
            
            return True
        
        else:

            return False
    
    def pre_load(self, dt):

        try:
                
            self._dict['nodes_origin'] = self.view_nodes(self.url_origin)

            self._dict['nodes_destin']= self.view_nodes(self.url_destin)

            self._dict['origin_prep'] = self.view_road('?q='+ str({'origin': self.perfil, 'status': 1}).replace("'",'"').replace(' ',''))['results']
        
            self._dict['origin_on_road'] = self.view_road('?q='+ str({'origin': self.perfil, 'status': 2}).replace("'",'"').replace(' ',''))['results']

            self._dict['destin_prep']= self.view_road('?q='+ str({'destination': self.perfil, 'status': 1}).replace("'",'"').replace(' ',''))['results']

            self._dict['destin_on_road']= self.view_road('?q='+ str({'destination': self.perfil, 'status': 2}).replace("'",'"').replace(' ',''))['results']

            self.dict= self._dict
            
        except: 

            pass
            
