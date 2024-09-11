from kivymd.uix.screen import MDScreen
from kivy.storage.jsonstore import JsonStore
from models import deco
from kivy.clock import mainthread
from kivymd.uix.dialog import MDDialog


class DialogIp(MDDialog):
    
    @mainthread
    def open_dilog(self, store):

        self.store= store

        self.open()

    @mainthread
    def close_card(self,):
        
        self.dismiss()     

    @deco
    def save_ip(self, url):
        
        try:
            url= url._get_text()

            self.store.put('url', ip= url)
        
        except:
            
            pass


class LoginScreen(MDScreen):
    
    store = JsonStore('load.json') 
    
    @deco
    def save_log(self, username, password):
        
        try:

            self.store.put('log', name= username, pswd= password)
        
        except:
            
            pass
    
    @mainthread
    def login_b(self,):
                  
        self.parent.parent.ids.btn_log.icon= 'logout'    

        self.parent.parent.ids.qr_btn.disabled= False
        
        self.parent.parent.ids.order_btn.disabled= False   
        
        self.parent.parent.ids.home_btn.disabled= False 
        
        self.parent.current= 'homescreen' 
        
        self.parent.parent.ids.home_screen.get_name()  
    
    @deco    
    def login_a(self, username, password):

        try:
           
            url= self.store.get('url')['ip']
                
            username= username._get_text()
                
            password= password._get_text()
            
            self.parent.user.log(url, username, password)
                               
            self.parent.user.pre_load()

            self.save_log(username, password)

            try:
            
                self.parent.user.printer = self.store.get('print')['print']
                
            except:
                
                pass
            
            self.login_b()
        
        except:
                
            self.parent.go_snack('Login incorrecto')

        self.parent.stop_progres(self)    

    def open_ipdialog(self):
        
        dialog= DialogIp()

        dialog.open_dilog(self.store)




        
        
