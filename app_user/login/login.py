from kivymd.uix.screen import MDScreen
from models import deco
from kivy.clock import mainthread

class LoginScreen(MDScreen):
    
    def save_log(self, username, password):
        
        try:

            self.manager.store.put('log', name= username, pswd= password)
        
        except:
            
            pass
    
    @mainthread
    def login_b(self,):
                  
        self.manager.parent.ids.btn_log.icon= 'logout'    

        self.manager.parent.ids.qr_btn.disabled= False
        
        self.manager.parent.ids.order_btn.disabled= False   
        
        self.manager.parent.ids.home_btn.disabled= False 
        
        self.manager.ids.home_screen.get_name()  

    @deco    
    def login_a(self,):

        try:
        
            url= self.manager.store.get('url')['ip']
                
            username= self.ids.username._get_text()
                
            password= self.ids.password._get_text()
            
            self.manager.user.log(url, username, password)

            self.manager.user.clock.schedule_once(self.manager.user.pre_load)
                                
            self.manager.event= self.manager.user.clock.schedule_interval(self.manager.user.pre_load, 60)

            self.save_log(username, password)
            
            self.login_b()

        except:

            self.manager.len_lists.append(False)






        
        
