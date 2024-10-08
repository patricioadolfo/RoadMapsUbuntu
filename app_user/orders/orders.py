from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemSupportingText, MDListItemTrailingCheckbox, MDListItemHeadlineText, MDListItemTertiaryText, MDListItemTrailingIcon

from kivy.clock import mainthread
from models import deco

class Order(MDScreen):

    @mainthread
    def clear_screen(self, list):

        for item in list:

            item.clear_widgets(item.children)
                
class OrderCreate(Order):
    
    def open_dialog(self,):

        try:

            self.manager.dialog_order(self.order_branch) 

        except:

            self.manager.go_snack('Indique el destino')      

    @mainthread
    def add_node(self, node):

        self.ids.mdlist.add_widget(MDListItem(
                                    MDListItemLeadingIcon(
                                        icon='map-marker-radius-outline',
                                            ),
                                            MDListItemSupportingText(
                                                text= node['name'],
                                            ),
                                            CheckB(
                                                    ),
                                            ripple_effect= False,
                                            ids= node
                                                )
                                                )

    @deco
    def branch_nodes(self,):

        try:
        
            self.clear_screen([self.ids.mdlist,],)

            if self.manager.user.id_user != {}:
                
                for node in self.manager.user.dict['nodes_origin']:

                    self.add_node(node)

        except:

            self.manager.len_lists.append(False)

    def on_checkbox_active(self, checkbox, value):
        
        if value:

            self.order_branch= checkbox.parent.parent.ids

class OrderScreenDealer(Order):
        
    def get_nodes(self, instance, *args):
        
        self.manager.go_screen(5, [self.manager.ids.order_screen_dealer_details.get_node_details(instance.ids)],'Error')

    @deco    
    def branch_nodes(self,):

        try:

            self.clear_screen([self.ids.mdlist])
                
            if self.manager.user.id_user != {}:

                for node in self.manager.user.dict['nodes_origin']:

                    self.view_nodes(node)
        except:

            self.manager.len_lists.append(False)
   
    def view_progress(self, instance, *args):

        self.manager.progress(self.manager.get_screen(self.manager.current))
    
    @mainthread
    def view_nodes(self, node):
                            
        self.ids.mdlist.add_widget(MDListItem(
            MDListItemLeadingIcon(
                icon='map-marker-radius-outline',
                    ),
                    MDListItemHeadlineText(
                        text= node['name'],
                    ),
                    MDListItemSupportingText(
                        text= node['address'],
                    ),
                    MDListItemTertiaryText(
                        text= node['phoneNumber'],
                    ),
                    MDListItemTrailingIcon(
                        icon="view-sequential-outline",
                    ),
                    ids= node,
                    ripple_effect= False,
                    on_press= self.view_progress,
                    on_release= self.get_nodes

                ))
                
class OrderScreenDealerDetails(Order):

    @mainthread
    def node_details(self, instance):
                     
        self.ids.branch_details_lb.text= instance['name']
        
        for item in self.prepared['results']:
            
            self.ids.branch_details_p.add_widget(MDListItem(
                                                    MDListItemHeadlineText(
                                                        text= '###'+ str(item['id']),
                                                    ),
                                                    MDListItemSupportingText(
                                                        text= '     Para: '+item['destination_name'],
                                                    ),
                                                    MDListItemTertiaryText(
                                                        text= '         Preparado: '+item['preparation_date'],
                                                    ),
                                                    MDListItemTrailingIcon(
                                                        icon="package-variant-closed-plus",
                                                    ),
                                                )
                                        )

        
        for item in self.on_road['results']:
            
            self.ids.branch_details_c.add_widget(MDListItem(
                                                        MDListItemHeadlineText(
                                                            text= '###'+ str(item['id']),
                                                            ),
                                                        MDListItemSupportingText(
                                                            text= '     De: '+item['origin_name'],
                                                            ),
                                                        MDListItemTertiaryText(
                                                            text= '         Preparado: '+item['preparation_date'],
                                                            ),
                                                        MDListItemTrailingIcon(
                                                            icon="package-variant-minus",
                                                            ),
                                                        )
                                                        )
        
    @deco
    def get_node_details(self, instance):
        
        try:    

            p= self.prepared= self.manager.user.view_road('?q='+ str({"status":1, "origin": instance['id']}).replace("'",'"').replace(' ',''))

            if p == False:

                self.manager.len_lists.append(False)                                                   
            
            c= self.on_road= self.manager.user.view_road('?q='+ str({"status":2, "destination": instance['id']}).replace("'",'"').replace(' ',''))
            
            if c == False:

                self.manager.len_lists.append(False)
                
            self.node_details(instance)
            
        except:
            
            self.manager.len_lists.append(False)
    
    @deco
    def back_branchsecreen(self, list):

        self.clear_screen(list)

class CheckB(MDListItemTrailingCheckbox):

    def check_active(self, checkbox, value):
        
        if value:
 
            self.parent.parent.parent.parent.parent.parent.parent.order_branch = checkbox.parent.parent.ids