from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemTertiaryText
from kivy.uix.behaviors import ButtonBehavior

from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.list import MDListItemTrailingIcon

from kivymd.uix.menu import MDDropdownMenu

class TrailingPressedIconButton(ButtonBehavior, RotateBehavior, MDListItemTrailingIcon):
    pass
       
class HomeScreen(MDScreen):
    
    origin_or_destin= ''

    def order_item(self, order, list):            
           
        item= MDListItem(
                        MDListItemLeadingIcon(
                            icon='package-variant-plus',
                                ),
                        MDListItemTertiaryText(
                            text= str(order['id'])+' Para '+ order['destination_name'] + ', preparado el '+ order['preparation_date']
                        ),
                        ripple_effect= False,
                        ids= order,

                    )
        list.add_widget(item)
                   
    def get_name(self,):

        self.ids.text_home.text= 'Hola '+ self.parent.user.id_user['username']

    def get_orders(self, state):  
      
        self.ids.list_send.clear_widgets(self.ids.list_send.children) 

        self.ids.list_receive.clear_widgets(self.ids.list_receive.children)   
            
        if state == 'p':
                
            for order in self.manager.user.dict['origin_prep']:

                self.order_item(order, self.ids.list_send)
            
            for order in self.manager.user.dict['destin_prep']:

                self.order_item(order, self.ids.list_receive)

            self.ids.text_state.text = 'ESTADO: PREPARADO EN SUCURSAL'

            self.ids.text_env.text = 'ENVIAR'

        elif state == 'c':
        
            for order in self.manager.user.dict['origin_on_road']:

                self.order_item(order, self.ids.list_send)
            
            for order in self.manager.user.dict['destin_on_road']:

                self.order_item(order, self.ids.list_receive)

            self.ids.text_state.text = 'ESTADO: EN CAMINO'

            self.ids.text_env.text = 'ENVIADO'
        else:

            self.parent.go_snack('Complete los campos')

    def menu_open(self):
        
        menu_items = [
            {"text": "PREPARADO EN SUCURSAL", "on_release": lambda x='p': self.get_orders(x)},
            {"text": "EN CAMINO", "on_release": lambda x='p': self.get_orders(x)}
        ]
        MDDropdownMenu(
            caller=self.ids.item_state, items=menu_items
        ).open()
    
 