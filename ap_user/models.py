import requests
from datetime import datetime
import time
import socket
import json
from threading import Thread


def deco(funcion):
    
    def envolvente(*args):
         
        thread = Thread(target=funcion, args=args)

        thread.start()
        
        return thread
        
    return envolvente

class Client():
    
    msj= {}
    
    ip= ''
    
    port= 0
    
    passwd= ''
    
    printer= ''
    
    def conect(self,):
                
        self.port = int(self.port)
        
        self.client_p= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.client_p.connect((self.ip, self.port))
        
        data = self.client_p.recv(2048).decode()
           
        self.printers= json.loads(data)

    def send(self, data):
        
        try:
            text= """ 
De: {origen}
Para: {destino}
Preprado el: {date} , {time}""".format(origen= data['origin_name'],
                                        destino= data['destination_name'], 
                                        date= data['preparation_date'], 
                                        time= data['preparation_time'] )
        
            msj= {'password': self.passwd, 'id': data['id'], 'text': text, 'printer': self.printer}
            
        except:
           msj= {'password': '', 'id': '', 'text': '', 'printer': ''}
            
        
        msj= json.dumps(msj)
            
        self.client_p.send(msj.encode())
          
    def disconnect(self,):
        
        self.client_p.close()

class Route:
    
    def __init__(self,):    
        
        pass
        
    def get_url(self, id= ''):

        r= self.client.get( self.url + id)

        if r.status_code == 200:
            
            return r.json()
        
        else:
            return 'Error!'
           
    def patch_url(self, id, payload):
        
        self.url= self.url +  id + '/'
        
        self.client.get(self.url)   

        if 'csrftoken' in self.client.cookies:
            
            csrftoken = self.client.cookies['csrftoken']
        
            p= self.client.patch(self.url, data= payload, headers={'X-CSRFTOKEN': csrftoken})
          
    def post_url(self, payload):
        
        self.client.get(self.url) 
        
        if 'csrftoken' in self.client.cookies:

            csrftoken = self.client.cookies['csrftoken']
            
            payload['csrfmiddlewaretoken']= csrftoken
            
            payload['next']= ''
            
            post= self.client.post(self.url, data= payload, headers=dict(Referer= self.url))
        
            return post.status_code

class User(Route, Client):
    
    def __init__(self,):
        
        self.id_user= {}
        
        self.dict= {}

        self._dict= {}

        self.time_preload= 60

        self.stop= False

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
        
        self.client = requests.session()
        
        self.client.get(self.url_login) 
        
        if 'csrftoken' in self.client.cookies:

            csrftoken = self.client.cookies['csrftoken']
            
            login_data = dict(username= user, password= passwd, csrfmiddlewaretoken=csrftoken, next='/api/api-user/')
            
            id = self.client.post(self.url_login, data=login_data, headers=dict(Referer= self.url_login))
        
            self.id_user= id.json()['results'][0]         

#            self.nodes_origin= self.view_nodes(self.url_origin)
            
#            self.nodes_destin= self.view_nodes(self.url_destin)
            
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
            
    def on_road(self, id_route):
        
        self.url= self.url_route
     
        payload= {"status":"r"}
    
        patch= self.patch_url(id_route, payload)
        
        payload={
            "route_id": id_route,
            "status": 'r',
            "instance_date":  datetime.today().strftime("%Y-%m-%d"),
            "instance_time": time.strftime("%H:%M:%S", time.localtime()),
            "user": self.id_user['id'],
            "route": id_route
        }
        
        self.url= self.url_instance

        self.post_url(payload)        
        
        return patch

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
                    "status": "p",
                    "user": self.id_user['id'],
                    "origin": self.perfil,
                    "destination": branch['id']
                  }        
        
        post= self.post_url(payload)
        
        return post
    
    def pre_load(self, dt):

        try:
                
            self._dict['nodes_origin'] = self.view_nodes(self.url_origin)

            self._dict['nodes_destin']= self.view_nodes(self.url_destin)

            self._dict['origin_prep'] = self.view_road('?q='+ str({'origin': self.perfil, 'status': 'p'}).replace("'",'"').replace(' ',''))['results']
        
            self._dict['origin_on_road'] = self.view_road('?q='+ str({'origin': self.perfil, 'status': 'c'}).replace("'",'"').replace(' ',''))['results']

            self._dict['destin_prep']= self.view_road('?q='+ str({'destination': self.perfil, 'status': 'p'}).replace("'",'"').replace(' ',''))['results']

            self._dict['destin_on_road']= self.view_road('?q='+ str({'destination': self.perfil, 'status': 'c'}).replace("'",'"').replace(' ',''))['results']

            self.dict= self._dict
            
        except: 

            pass
            
