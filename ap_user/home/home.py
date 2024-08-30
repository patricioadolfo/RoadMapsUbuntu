from kivymd.uix.screen import MDScreen
from models import deco
from kivy.clock import mainthread

from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemTertiaryText


       
class HomeScreen(MDScreen):
    
    dict_query= {}

    def order_item(self, order):            
           
        item= MDListItem(
                        MDListItemLeadingIcon(
                            icon='package-variant-plus',
                                ),
                        MDListItemTertiaryText(
                            text= str(order['id'])+' Para '+ order['destination_name'] + ', preparado el '+ order['preparation_date']
                        ),
                        ids= order,

                    )
        self.ids.mdlist.add_widget(item)
                   
    def get_name(self,):

        self.ids.text_home.text= 'Hola '+ self.parent.user.id_user['username']

    def origin_or_destin(self, o_d):

        if o_d == 'o':

            if 'destination' in self.dict_query:
                
                del self.dict_query['destination']

            self.dict_query['origin']= self.parent.user.perfil

        elif o_d == 'd':

            if 'origin' in self.dict_query:
                
                del self.dict_query['origin']

            self.dict_query['destination']= self.parent.user.perfil
        
        else:
            pass

    def get_orders(self, state):  
      
        self.ids.mdlist.clear_widgets(self.ids.mdlist.children)   

        if state == 'c':
            self.dict_query['status']= 'c'

        elif state == 'p':
            self.dict_query['status']= 'p'

        else: 
            pass

        if 'destination' in self.dict_query:

            self.parent.list= self.parent.user.view_road('?q='+ str(self.dict_query).replace("'",'"').replace(' ',''))

            for order in self.parent.list['results']:

                self.order_item(order)
        
        elif 'origin' in self.dict_query:

            self.parent.list= self.parent.user.view_road('?q='+ str(self.dict_query).replace("'",'"').replace(' ',''))

        
            for order in self.parent.list['results']:

                self.order_item(order)

        else: 
            self.parent.go_snack('Complete los campos')
