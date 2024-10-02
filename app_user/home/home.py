from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemTertiaryText
from kivy.clock import mainthread
from kivymd.uix.menu import MDDropdownMenu
from models import deco

class HomeScreen(MDScreen):

    def open_dialog(self, instance, *args):

        self.manager.dialog_home()

        self.manager.dialog.text_card(instance.ids)

    @mainthread
    def clear_list(self,):

        self.ids.list_send.clear_widgets(self.ids.list_send.children) 

        self.ids.list_receive.clear_widgets(self.ids.list_receive.children) 

        self.menu.dismiss()

    @mainthread
    def set_text(self,text_state, text_env):

        self.ids.text_state.text = text_state

        self.ids.text_env.text= text_env

    @mainthread
    def order_item(self, order, list, p_c):

        if p_c == 1:

            text_list=  str(order['id'])+' Para '+ order['destination_name'] + ', preparado el '+ order['preparation_date']

        else:

            text_list= str(order['id'])+' De '+ order['origin_name'] + ', preparado el '+ order['preparation_date']           
           
        item= MDListItem(
                        MDListItemLeadingIcon(
                            icon='package-variant-plus',
                                ),
                        MDListItemTertiaryText(
                            text= text_list
                        ),
                        ripple_effect= False,
                        on_press= self.open_dialog, 
                        ids= order,

                    )
        list.add_widget(item)
                   
    def get_name(self,):

        self.ids.text_home.text= 'Hola '+ self.manager.user.id_user['username']
   
    @deco
    def get_orders(self, state):  
  
        try:

            self.clear_list()
    
            if state == 1:
                    
                for order in self.manager.user.dict['origin_prep']:

                    self.order_item(order, self.ids.list_send, 1)
                
                for order in self.manager.user.dict['destin_prep']:

                    self.order_item(order, self.ids.list_receive, 2)
                
                self.set_text('ESTADO: PREPARADO EN SUCURSAL', 'ENVIAR')

            elif state == 2:
            
                for order in self.manager.user.dict['origin_on_road']:

                    self.order_item(order, self.ids.list_send, 1)
                
                for order in self.manager.user.dict['destin_on_road']:

                    self.order_item(order, self.ids.list_receive, 2)

                self.set_text('ESTADO: EN CAMINO', 'ENVIADO')

        except:

            self.manager.len_lists.append(False)

    @mainthread
    def menu_open(self):
        
        menu_items = [
            {
            "text": "PREPARADO EN SUCURSAL",
            "on_press:": lambda: self.manager.progress(self.manager.get_screen(self.manager.current)),
            "on_release": lambda x=1: self.manager.go_screen(self.manager.current, [self.get_orders(x)], 'Error')
            },
            {
            "text": "EN CAMINO", 
            "on_press:": lambda: self.manager.progress(self.manager.get_screen(self.manager.current)),
            "on_release": lambda x=2: self.manager.go_screen(self.manager.current, [self.get_orders(x)], 'Error')
            }
        ]
        
        self.menu= MDDropdownMenu(
            caller=self.ids.item_state, 
            items=menu_items,
            position="bottom"
        )

        self.menu.open()
    
 