from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemHeadlineText, MDListItemSupportingText, MDListItemTertiaryText, MDListItemTrailingIcon
from models import deco
from kivy.clock import mainthread


class BranchScreen(MDScreen):
        
    def get_nodes(self, instance, *args):
        
        self.manager.go_screen('branchdetailsscreen', [self.manager.parent.ids.branch_details.get_node_details(instance.ids)],'Error')

    @deco    
    def branch_nodes(self,):

        try:

            self.clear_screen()
                
            if self.manager.user.id_user != {}:

                for node in self.manager.user.dict['nodes_origin']:

                    self.view_nodes(node)
        except:

            self.manager.len_lists.append(False)

    @mainthread
    def clear_screen(self,):

        self.ids.mdlist.clear_widgets(self.ids.mdlist.children)
    
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


                
class BranchDetails(MDScreen):

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

            self.prepared= self.manager.user.view_road('?q='+ str({"status":"p", "origin": instance['id']}).replace("'",'"').replace(' ',''))
                                                                 
            self.on_road= self.manager.user.view_road('?q='+ str({"status":"c", "destination": instance['id']}).replace("'",'"').replace(' ',''))
            
            self.node_details(instance)
            
        except:
            
            self.manager.len_lists.append(False)
    
    @mainthread
    def back_branchsecreen(self, *args):
            
        self.ids.branch_details_p.clear_widgets(self.ids.branch_details_p.children)
        
        self.ids.branch_details_c.clear_widgets(self.ids.branch_details_c.children)
        
        self.parent.current= 'branchscreen'