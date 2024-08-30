from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemHeadlineText, MDListItemTrailingCheckbox
from kivymd.uix.menu import MDDropdownMenu
from models import deco
from kivy.clock import mainthread
from kivymd.uix.dialog import MDDialog

class CheckB(MDListItemTrailingCheckbox):
    
    def check_active(self, checkbox, value):
        
        if value:
 
            self.parent.parent.parent.parent.parent.parent.parent.order_branch = checkbox.parent.parent.ids

class DialogCreate(MDDialog):

    def open_dialog(self, user, branch):

        self.user= user

        self.branch= branch

        self.open()

    def create_order(self, text):  

        self.text=  text._get_text()

        if self.text == '':
             pass
        
        else:

            try: 

                create = self.user.route_create(self.text, self.branch)

                if create == 400:
                    
                    pass
    
                    
                else:
                    
                    self.dismiss()
                                
            except:
                
                pass

class OrderCreate(MDScreen):
    
    @mainthread
    def open_dialog(self,):

        self.dialog= DialogCreate()

        try:

            self.dialog.open_dialog(self.manager.user, self.order_branch) 

        except:

            self.manager.go_snack('Indique el destino')      
                    
    def branch_nodes(self,):
           
        self.ids.mdlist.clear_widgets(self.ids.mdlist.children)
        
        if self.manager.user.id_user != {}:
        
            nodes= self.manager.user.nodes_origin
            
            for node in nodes:
                
                self.ids.mdlist.add_widget(MDListItem(
                                                    MDListItemLeadingIcon(
                                                        icon='map-marker-radius-outline',
                                                            ),
                                                            MDListItemHeadlineText(
                                                                text= node['name'],
                                                            ),
                                                            CheckB(
                                                                    ),
                                                            ids= node
                                                                )
                                                                )

    def on_checkbox_active(self, checkbox, value):
        
        if value:

            self.order_branch= checkbox.parent.parent.ids

