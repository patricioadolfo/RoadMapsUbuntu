from kivymd.uix.dialog import MDDialog
from kivy.clock import mainthread
from models import deco

class HomeDialog(MDDialog):
    
    @mainthread
    def dialog_open(self):
        
        self.open()

    @deco       
    def text_card(self, dict):
                
        self.ids.text_header.text = str(dict['id'])
        
        self.ids.lb_box_card.text= dict['description']

        if dict['another_origin'] != None:

            self.ids.origin_dialog.text= 'De '+ dict['another_origin_name']
        
        else:
            
            self.ids.origin_dialog.text= 'De '+ dict['origin_name']

        if dict['another_destin'] != None:

            self.ids.destin_dialog.text=  'Para '+ dict['another_destin_name']

        else:            
            
            self.ids.destin_dialog.text=  'Para '+ dict['destination_name']

        self.dialog_open()
                                 
    @mainthread
    def close_dialog(self,):
        
        self.dismiss()      

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

class QrDialog(MDDialog):
    
    @mainthread
    def qr_open(self):
        
        self.open()
           
    def text_card(self, dict, manager):
        
        self.dict= dict
        
        self.manager= manager 
                
        detail_text= self.status(dict)
        
        self.ids.lb_box_card.text= detail_text
        
        if 'origin_name' in dict:

            if dict['another_origin'] != None:
            
                self.ids.origin_dialog.text= 'De '+ dict['another_origin_name']
            
            else:

                self.ids.origin_dialog.text= 'De '+ dict['origin_name']

            if dict['another_destin'] != None:

                self.ids.destin_dialog.text=  'Para '+ dict['another_destin_name']
            
            else:
                
                self.ids.destin_dialog.text=  'Para '+ dict['destination_name']
                                 
    @mainthread
    def close_card(self,):
        
        self.dismiss()      
            
    def status(self, dict):
        
        if 'status' in dict:
        
            if dict['status'] == 2:

                if self.manager.user.perfil == None:

                    if dict['another_destin'] != None:

                        self.buton_status(False)
                    
                    else:

                        self.buton_status(True)
                    
                    detail_text= 'Envio n° {id} en camino'.format(id= str(dict['id']))

                else:

                    self.buton_status(False)
                    
                    detail_text= 'Envio n° {id}, preparado el dia {date} a las {time}'.format(
                        id= str(dict['id']),
                        date= dict['preparation_date'],
                        time= dict['preparation_time'],
                    ) 
            
            elif dict['status'] == 1:

                if self.manager.user.perfil == None: 

                    self.buton_status(False)
                
                    detail_text= 'Envio n° {id}, preparado el dia {date} a las {time}'.format(
                                                                                        id= str(dict['id']),
                                                                                        date= dict['preparation_date'],
                                                                                        time= dict['preparation_time'],
                                                                                           ) 


                else:
                    
                    detail_text= 'Envio n° {id} preparado'.format(id= str(dict['id']))

            
            elif dict['status'] == 3:

                detail_text= 'Envio n° {id} recibido'.format(id= str(dict['id']))
            
            elif dict['status'] == 8:

                detail_text= 'Envio n° {id} entregado'.format(id= str(dict['id']))

            else:
                detail_text= 'Ocurrio algún error'
            
            return detail_text
        
        if 'qr' in dict:
            
            detail_text= dict['qr'] + '\n' + dict['msj']
            
            return detail_text
    
    @mainthread
    def buton_status(self, state):

        self.ids.btn_rec.disabled = state

    @deco        
    def receive_route(self):

        if self.manager.user.perfil != None:

            if self.dict['destination'] == self.manager.user.perfil:

                receive= self.manager.user.receive(str(self.dict['id']), 3)

                if receive == True:
                
                    self.close_card()

                    self.buton_status(True)

                    self.manager.go_snack('Envio '+ str(self.dict['id']) + ' recibido')
                
                else:
                
                    self.manager.len_lists.append(False)

            else:

                self.manager.go_snack('El envío es para '+ self.dict['destination_name'])

        else:

            if self.dict['another_destin'] != None:

                if self.dict['status'] == 2:
           
                    receive= self.manager.user.receive(str(self.dict['id']), 8)
                
                else:

                    receive= self.manager.user.receive(str(self.dict['id']), 2)
            
            else:

                receive= self.manager.user.receive(str(self.dict['id']), 2)
                
            if receive == True:
                
                self.close_card()

                self.buton_status(True)

                self.manager.go_snack('Envio '+ str(self.dict['id']) + ' recibido')
                
            else:
                
                self.manager.len_lists.append(False)

class DialogIp(MDDialog):
    
    @mainthread
    def open_dilog(self, store):

        self.store= store

        self.open()

    @mainthread
    def close_card(self,):
        
        self.dismiss()     

    @deco
    def save_ip(self, url):
        
        try:
            url= url._get_text()

            self.store.put('url', ip= url)
        
        except:
            
            pass