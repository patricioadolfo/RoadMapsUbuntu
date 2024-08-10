from kivymd.uix.screen import MDScreen
from kivy.storage.jsonstore import JsonStore
from models import deco
from kivy.clock import mainthread


class LoginScreen(MDScreen):
    
    store = JsonStore('load.json') 
    
    def save_log(self, username, password, url):

        try:
            
            self.store.put('log', name= username, pswd= password, ip= url)
            
        except:
            
            pass
    
    @mainthread
    def login_b(self,):
                  
        self.parent.parent.ids.btn_log.icon= 'logout'    

        self.parent.parent.ids.qr_btn.disabled= False
        
        self.parent.parent.ids.order_btn.disabled= False   
        
        self.parent.parent.ids.home_btn.disabled= False 
        
        self.parent.current= 'homescreen' 
        
        self.parent.parent.ids.home_screen.order_list()  
    
    @deco    
    def login_a(self, url, username, password):

        try:
           
            url= url._get_text()
                
            username= username._get_text()
                
            password= password._get_text()
            
            self.parent.user.log(url, username, password)
                               
            self.save_log(username, password, url)
            
            self.parent.on_road= self.parent.user.view_road('?q='+ str({"status":"c", "origin": self.parent.user.perfil}).replace("'",'"').replace(' ',''))

            self.parent.receiver= self.parent.user.view_road('?q='+ str({"status":"p", "origin": self.parent.user.perfil}).replace("'",'"').replace(' ',''))
            
            try:
            
                self.parent.user.printer = self.store.get('print')['print']
                
            except:
                
                pass
            
            self.login_b()
            
            self.parent.stop_progres(self)
        
        except:
                
            self.children[-1].text= 'Login Incorrecto'
            
            self.parent.stop_progres(self)






        
        
