from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemSupportingText, MDListItemTrailingCheckbox
from kivy.clock import mainthread
from kivymd.uix.dialog import MDDialog

class CheckB(MDListItemTrailingCheckbox):

    def check_active(self, checkbox, value):
        
        if value:
 
            self.parent.parent.parent.parent.parent.parent.parent.order_branch = checkbox.parent.parent.ids

class DialogCreate(MDDialog):

    def open_dialog(self, manager, branch):

        self.manager= manager

        self.branch= branch

        self.open()

    def create_order(self, text):  

        self.text=  text._get_text()

        if self.text == '':
             
             self.manager.go_snack('Describa su envío')
        
        else:

            try: 

                create = self.manager.user.route_create(self.text, self.branch)

                if create == 400:
                    
                    self.manager.go_snack('Error de conexión')
                       
                else:
                    self.manager.go_snack('Envío creado con éxito')
                    
                    self.dismiss()
                                
            except:
                
                self.manager.go_snack('Error de conexión')

                self.dismiss()

class OrderCreate(MDScreen):
    
    @mainthread
    def open_dialog(self,):

        self.dialog= DialogCreate()

        try:

            self.dialog.open_dialog(self.manager, self.order_branch) 

        except:

            self.manager.go_snack('Indique el destino')      
                    
    def branch_nodes(self,):
           
        self.ids.mdlist.clear_widgets(self.ids.mdlist.children)
        
        if self.manager.user.id_user != {}:
            
            for node in self.manager.user.dict['nodes_origin']:
                
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

    def on_checkbox_active(self, checkbox, value):
        
        if value:

            self.order_branch= checkbox.parent.parent.ids

