from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemTertiaryText


       
class HomeScreen(MDScreen):
    
    origin_or_destin= ''

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

    def get_orders(self, state):  
      
        self.ids.mdlist.clear_widgets(self.ids.mdlist.children)   
            
        if self.origin_or_destin == 'o':

            if state == 'p':
                    
                query= self.manager.user.dict['origin_prep']

            else:
                    
                query = self.manager.user.dict['origin_on_road']

            for order in query:

                self.order_item(order)
            
        elif self.origin_or_destin == 'd':

            if state == 'p':

                query= self.manager.user.dict['destin_prep']

            else:

                query= self.manager.user.dict['destin_on_road']
 
            for order in query:

                self.order_item(order)

        else: 

            self.parent.go_snack('Complete los campos')


        
 