from kivymd.uix.screen import MDScreen
from kivymd.uix.badge import MDBadge
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemTertiaryText
from kivy.clock import mainthread
from kivymd.uix.menu import MDDropdownMenu
from models import deco

class Home(MDScreen):

    def open_dialog(self, instance, *args):

        self.manager.dialog_home()

        self.manager.dialog.text_card(instance.ids)

    def get_name(self,):

        self.ids.text_home.text= 'Hola '+ self.manager.user.id_user['username']

    @mainthread
    def order_item(self, order, list, o_or_d):    

        try:       
            
            t= str(order['id'])+ o_or_d[0] + order[o_or_d[1]] + ', preparado el '+ order['preparation_date']

            item= MDListItem(
                            MDListItemLeadingIcon(
                                icon='package-variant-plus',
                                    ),
                            MDListItemTertiaryText(
                                text= t
                            ),
                            ripple_effect= False,
                            on_press= self.open_dialog,
                            ids= order,

                        )
            list.add_widget(item)
        
        except:
            
            pass

class HomeScreen(Home):

    @mainthread
    def clear_list(self,):

        self.ids.list_send.clear_widgets(self.ids.list_send.children) 

        self.ids.list_receive.clear_widgets(self.ids.list_receive.children) 

        self.menu.dismiss()

    @mainthread
    def set_text(self,text_state, text_env):

        self.ids.text_state.text = text_state

        self.ids.text_env.text= text_env
                      
    @deco
    def get_orders(self, state):  
  
        try:

            self.clear_list()
    
            if state == 1:
      
                for order in self.manager.user.dict['origin_prep']:

                    if order['another_destin'] != None:

                        self.order_item(order, self.ids.list_send,[' Para ', 'another_destin_name'])

                    else:

                        self.order_item(order, self.ids.list_send,[' Para ', 'destination_name'])
            
                for order in self.manager.user.dict['destin_prep']:

                    if order['another_origin'] != None:

                        self.order_item(order, self.ids.list_receive, [' De ', 'another_origin_name'])
                    
                    else:

                        self.order_item(order, self.ids.list_receive, [' De ', 'origin_name'])
            
                self.set_text('ESTADO: PREPARADO EN SUCURSAL', 'ENVIAR')

            elif state == 2:              

                for order in self.manager.user.dict['origin_on_road']:
                    
                    if order['another_destin'] != None:

                        self.order_item(order, self.ids.list_send, [' Para ', 'another_destin_name'])
                
                    else:

                        self.order_item(order, self.ids.list_send, [' Para ', 'destination_name'])
                
                
                for order in self.manager.user.dict['destin_on_road']:

                    if order['another_origin'] != None:

                        self.order_item(order, self.ids.list_receive, [' De ', 'another_origin_name'])

                    else:

                        self.order_item(order, self.ids.list_receive, [' De ', 'origin_name'])

                self.set_text('ESTADO: EN CAMINO', 'ENVIADO')

        except:

            self.manager.len_lists.append(False)

    @mainthread
    def menu_open(self):
        
        menu_items = [
            {
            "text": "PREPARADO EN SUCURSAL",
            "on_press:": lambda: self.manager.progress(self.manager.get_screen(self.manager.current)),
            "on_release": lambda x=1: self.manager.go_screen(1, [self.get_orders(x)], 'Error')
            },
            {
            "text": "EN CAMINO", 
            "on_press:": lambda: self.manager.progress(self.manager.get_screen(self.manager.current)),
            "on_release": lambda x=2: self.manager.go_screen(1, [self.get_orders(x)], 'Error')
            }
        ]
        
        self.menu= MDDropdownMenu(
            caller=self.ids.item_state, 
            items=menu_items,
            position="bottom"
        )

        self.menu.open()
    
class HomeScreenDealer(Home):
    
    @mainthread
    def clear_list(self,):

        self.ids.list_prepared.clear_widgets(self.ids.list_prepared.children) 

        self.ids.list_onroad.clear_widgets(self.ids.list_onroad.children) 

        self.ids.icon_prep.clear_widgets(self.ids.icon_prep.children)

        self.ids.icon_onroad.clear_widgets(self.ids.icon_onroad.children)

    @mainthread
    def set_text(self,):

        p = str(self.manager.user.dict['prepared']['count'])

        badge_p= MDBadge()

        badge_p.text= p

        self.ids.icon_prep.add_widget(badge_p)

        self.ids.text_prepared.text = f'Tienes {p} pedidos preparados para retirar'

        c = str(self.manager.user.dict['on_road']['count'])

        badge_c= MDBadge()

        badge_c.text= c

        self.ids.icon_onroad.add_widget(badge_c)

        self.ids.text_onroad.text= f'Tienes {c} pedidos en camino para entregar'
  
    @deco
    def get_orders(self,):  
            
        try:

            self.clear_list()
            
            for order in self.manager.user.dict['prepared']['results']:

                if order['another_origin'] != None:

                    self.order_item(order, self.ids.list_prepared, [' de ', 'another_origin_name'])

                else:

                    self.order_item(order, self.ids.list_prepared, [' de ', 'origin_name'])
                
            for order in self.manager.user.dict['on_road']['results']:

                if order['another_destin'] != None:

                    self.order_item(order, self.ids.list_onroad, [' para ', 'another_destin_name'])

                else:

                    self.order_item(order, self.ids.list_onroad, [' para ', 'destination_name'])
                
            self.set_text()

        except:

            self.manager.len_lists.append(False)