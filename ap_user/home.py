from kivymd.uix.screen import MDScreen
from models import deco
from kivy.clock import mainthread

from kivymd.uix.badge import MDBadge
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemHeadlineText, MDListItemTertiaryText, MDListItemTrailingIcon
from kivymd.uix.divider import MDDivider

       
class HomeScreen(MDScreen):
    
    def order_item(self, order, list):
           
        item= MDListItem(
                        MDListItemLeadingIcon(
                            icon='package-variant-plus',
                                ),
                        MDListItemTertiaryText(
                            text= str(order['id'])+' Para '+ order['destination_name'] + ', preparado el '+ order['preparation_date']
                        ),
                        ids= order,

                    )
        list.add_widget(item)
    
    @mainthread        
    def order_list(self,):
        
        self.ids.text_home.text= 'Hola '+ self.parent.user.id_user['username'] 
               
        self.ids.mdlist.clear_widgets(self.ids.mdlist.children)
        
        try:
        
            if self.parent.user.id_user != {}:
                        
                self.ids.mdlist.add_widget(
                    MDListItem(
                        MDListItemHeadlineText(
                            text= 'Mis pedidos EN CAMINO',
                            halign= "center"
                            
                            ), 
                        MDListItemTrailingIcon(
                            MDBadge(
                            text= str(self.parent.on_road['count'])  
                            ),
                            icon= 'information-variant',
                        )
                    )
                )
                
                self.ids.mdlist.add_widget(MDDivider())
                
                for order in self.parent.on_road['results']:

                    self.order_item(order, self.ids.mdlist)
                
                self.ids.mdlist.add_widget(
                    MDListItem(
                        MDListItemHeadlineText(
                            text= 'Mis pedidos PREPARADOS',
                            halign= "center"
                            ), 
                        MDListItemTrailingIcon(
                            MDBadge(
                            text= str(self.parent.receiver['count'])  
                            ),
                            icon= 'information-variant',
                        )
                    )
                )
                
                self.ids.mdlist.add_widget(MDDivider())
                
                for order in self.parent.receiver['results']:

                    self.order_item(order, self.ids.mdlist)
        
        except:
            
            self.parent.go_snack('Error de conexión')
               
    @deco
    def get_order(self,):
        
        try:
            
            self.parent.on_road= self.parent.user.view_road('?q='+ str({"status":"c", "origin": self.parent.user.perfil}).replace("'",'"').replace(' ',''))

            self.parent.receiver= self.parent.user.view_road('?q='+ str({"status":"p", "origin": self.parent.user.perfil}).replace("'",'"').replace(' ',''))

            self.order_list()
            
            self.parent.stop_progres(self)
        
        except:
            
            self.parent.go_snack('Error de conexión')
            
            self.parent.stop_progres(self)
            
            

        



