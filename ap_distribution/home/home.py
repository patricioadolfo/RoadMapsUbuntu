from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemTertiaryText
from kivy.clock import mainthread
from kivymd.uix.badge import MDBadge

from models import deco


class HomeScreen(MDScreen):
    
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

    @mainthread
    def order_item(self, order, list, o_or_d):            
           
        item= MDListItem(
                        MDListItemLeadingIcon(
                            icon='package-variant-plus',
                                ),
                        MDListItemTertiaryText(
                            text= str(order['id'])+ o_or_d[0] + order[o_or_d[1]] + ', preparado el '+ order['preparation_date']
                        ),
                        ripple_effect= False,
                        ids= order,

                    )
        list.add_widget(item)
                   
    def get_name(self,):

        self.ids.text_home.text= 'Hola '+ self.manager.user.id_user['username']
   
    @deco
    def get_orders(self,):  
            
        try:

            self.clear_list()
            
            for order in self.manager.user.dict['prepared']['results']:

                self.order_item(order, self.ids.list_prepared, [' de ', 'origin_name'])
                
            for order in self.manager.user.dict['on_road']['results']:

                self.order_item(order, self.ids.list_onroad, [' para ', 'destination_name'])
                
            self.set_text()

        except:

            self.manager.len_lists.append(False)


    
 