from kivymd.uix.screen import MDScreen
from kivy.storage.jsonstore import JsonStore
from models import deco
from kivy.clock import mainthread
from kivymd.uix.dialog import MDDialog
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

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
    
    def save_log(self, username, password):
        
        try:

            self.store.put('log', name= username, pswd= password)
        
        except:
            
            pass
    
    @mainthread
    def login_b(self,):
                  
        self.manager.parent.ids.btn_log.icon= 'logout'    

        self.manager.parent.ids.qr_btn.disabled= False
        
        self.manager.parent.ids.branch_btn.disabled= False   
        
        self.manager.parent.ids.home_btn.disabled= False 
        
        self.manager.parent.ids.home_screen.get_name() 

        self.manager.parent.ids.home_screen.get_orders()  

    @deco    
    def login_a(self,):

        try:
        
            url= self.store.get('url')['ip']
                
            username= self.ids.username._get_text()
                
            password= self.ids.password._get_text()
            
            self.manager.user.log(url, username, password)

            self.manager.user.clock.schedule_once(self.manager.user.pre_load)
                                
            self.manager.event= self.manager.user.clock.schedule_interval(self.manager.user.pre_load, 60)

            self.save_log(username, password)

            try:
            
                self.manager.user.printer = self.store.get('print')['print']
                
            except:
                
                pass
            
            self.login_b()

        except:

            self.manager.len_lists.append(False)

    def open_ipdialog(self):
        
        dialog= DialogIp()

        dialog.open_dilog(self.store)




        
        
