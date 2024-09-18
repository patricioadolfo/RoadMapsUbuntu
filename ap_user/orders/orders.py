from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemSupportingText, MDListItemTrailingCheckbox
from kivy.clock import mainthread
from kivymd.uix.dialog import MDDialog
from models import deco

class DialogCreate(MDDialog):

    @mainthread
    def open_dialog(self, manager, branch):

        self.manager= manager

        self.branch= branch

        self.open()

    @deco
    def create_order(self,):  

        try:

            self.text=  self.ids.text_detail._get_text()

            if self.text == '':
                
                self.manager.go_snack('Describa su envío')
            
            else:

                create = self.manager.user.route_create(self.text, self.branch)

                if create == 400:
                    
                    self.manager.go_snack('Error al crear pedido')
                    
                else:

                    name= self.branch['name']

                    self.manager.go_snack(f'Envío para {name}, creado con éxito')
                    
                    self.dismiss()

        except:
            
            self.manager.len_lists.append(False)

class OrderCreate(MDScreen):
    
    @mainthread
    def open_dialog(self,):

        self.dialog= DialogCreate()

        try:

            self.dialog.open_dialog(self.manager, self.order_branch) 

        except:

            self.manager.go_snack('Indique el destino')      

    @mainthread
    def clear_nodes(self,):

        self.ids.mdlist.clear_widgets(self.ids.mdlist.children)

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
        
            self.clear_nodes()

            if self.manager.user.id_user != {}:
                
                for node in self.manager.user.dict['nodes_origin']:

                    self.add_node(node)

        except:

            self.manager.len_lists.append(False)

    def on_checkbox_active(self, checkbox, value):
        
        if value:

            self.order_branch= checkbox.parent.parent.ids

class CheckB(MDListItemTrailingCheckbox):

    def check_active(self, checkbox, value):
        
        if value:
 
            self.parent.parent.parent.parent.parent.parent.parent.order_branch = checkbox.parent.parent.ids