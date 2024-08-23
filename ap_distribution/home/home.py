from kivymd.uix.screen import MDScreen
from kivymd.uix.badge import MDBadge
from models import deco
from kivy.clock import mainthread
           
class HomeScreen(MDScreen):
    
    @mainthread
    def count_routes(self,):

        self.ids.text_home.text= 'Hola '+ self.parent.user.id_user['username'] 
        
        badge= MDBadge()
        
        badge.text= str(self.parent.prepared['count'] )
        
        if self.parent.prepared['count'] != 0:
            
            if self.ids.icon_prep.children == []:

                self.ids.icon_prep.add_widget(badge)                
        
            self.ids.text_prepared.text='Tienes '+ str(self.parent.prepared['count']) + ' pedidos preparados para retirar'
        
        else: 
            
            if self.ids.icon_prep.children != []:
                
                self.ids.icon_prep.clear_widgets(self.ids.icon_prep.children)
                
            self.ids.text_prepared.text='No tienes pedidos preparados para retirar' 

        badge_p= MDBadge()
        
        badge_p.text= str(self.parent.on_road['count'] )
        
        if self.parent.on_road['count'] != 0:
            
            if self.ids.icon_onroad.children == []:
                
                self.ids.icon_onroad.add_widget(badge_p)

            self.ids.text_onroad.text='Tienes '+ str(self.parent.on_road['count']) + ' pedidos en camino para entregar'
        
        else: 
            
            if self.ids.icon_onroad.children != []:
                
                self.ids.icon_onroad.clear_widgets(self.ids.icon_onroad.children)
                
            self.ids.text_onroad.text='No tienes pedidos en camino para entregar' 
        
    @deco
    def get_count(self,):

        try:
            
            self.parent.prepared= self.parent.user.view_road('?q='+ str({"status":"p"}).replace("'",'"').replace(' ',''))
            
            self.parent.on_road= self.parent.user.view_road('?q='+ str({"status":"c"}).replace("'",'"').replace(' ',''))

            self.count_routes()
            
            self.parent.stop_progres(self)
        
        except:
            
            self.parent.go_snack('Error de conexión')
            
            self.parent.stop_progres(self)