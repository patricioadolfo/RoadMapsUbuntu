from camera4kivy import Preview
from PIL import Image
from pyzbar.pyzbar import decode
from kivy.clock import mainthread

from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemHeadlineText, MDListItemSupportingText, MDListItemTertiaryText, MDListItemTrailingCheckbox

from time import sleep
from models import deco

class Check(MDListItemTrailingCheckbox):
    pass

class QrPrinter(MDScreen):
      
    def print_order(self, instance, *args):
        
        try:
            self.parent.user.conect()
            
            self.parent.user.send(instance.ids)
            
            self.parent.user.disconnect()
            
        except:
            
            self.parent.go_snack('Error de conexión')
    
    def order_item(self, order, list):
           
        item= MDListItem(
                        MDListItemLeadingIcon(
                            icon='printer',
                                ),
                        MDListItemSupportingText(
                            text= '## '+ str(order['id']),
                        ),
                        MDListItemTertiaryText(
                            text= 'Para '+ order['destination_name'] + ', preparado el '+ order['preparation_date']
                        ),
                        ids= order,
                        on_press= self.print_order
                    )
        list.add_widget(item)
    
    @deco
    def get_prepared(self):
        
        try:
            if self.parent.user.id_user != {}:
                
                self.prepared= self.parent.user.view_road('?q='+ str({"status":"p", "origin": self.parent.user.perfil}).replace("'",'"').replace(' ',''))

                self.list_orders()
                
        except:
            
            self.parent.go_snack('Error de conexión')
    
    @mainthread
    def list_orders(self,):
        
        self.ids.mdlist.clear_widgets(self.ids.mdlist.children)
       
        for order in self.prepared['results']:

            self.order_item(order, self.ids.mdlist)
                 
    def conect_printer(self,):
        
        try:
            self.parent.user.conect()
            
            self.parent.user.send({'password':''})
            
            self.parent.user.disconnect()
        
        except:
            
            self.parent.go_snack('Error de conexión')
            
    def list_printers(self,):
        
        self.ids.mdlist.clear_widgets(self.ids.mdlist.children)
        
        try:
        
            for printer in self.parent.user.printers:
        
                self.ids.mdlist.add_widget(MDListItem(
                                                    MDListItemLeadingIcon(  
                                                        icon= 'printer'),
                                                    MDListItemHeadlineText(
                                                        text= str(printer[0]),
                                                        ),
                                                    MDListItemSupportingText(
                                                        text= printer[1],
                                                        ),
                                                    MDListItemTertiaryText(
                                                        text= printer[2],
                                                        ),
                                                    Check(
                                                        ),
                                                    ))
        except:
            
            self.parent.go_snack('Error de conexión')

class QrDialog(MDDialog):
    
    @mainthread
    def qr_open(self):
        
        self.open()
           
    def text_card(self, dict, user):
        
        self.dict= dict
        
        self.user= user 
                
        detail_text= self.status(dict)
        
        self.ids.lb_box_card.text= detail_text
        
        if 'origin_name' in dict:
            
            self.ids.origin_dialog.text= 'De '+ dict['origin_name']
            
            self.ids.destin_dialog.text=  'Para '+ dict['destination_name']
                                 
    @mainthread
    def close_card(self,):
        
        self.dismiss()      
                
    def status(self, dict):
        
        if 'status' in dict:
        
            if dict['status'] == 'c':
                
                self.ids.btn_rec.disabled= False
                
                detail_text= 'Envio n° {id}, preparado el dia {date} a las {time}'.format(
                    id= str(dict['id']),
                    date= dict['preparation_date'],
                    time= dict['preparation_time'],
                ) 
            
            elif dict['status'] == 'p':
                detail_text= 'Envio n° {id} preparado'.format(id= str(dict['id']))
            
            else:
                detail_text= 'Envio n° {id} recibido'.format(id= str(dict['id']))
            
            return detail_text
        
        if 'qr' in dict:
            
            detail_text= dict['qr'] + '\n' + dict['msj']
            
            return detail_text
    
    @deco        
    def receive_route(self):
        
        try:
    
            self.user.on_road(str(self.dict['id']))
            
            self.close_card()
            
        except:
            
            self.parent.go_snack('Error de conexión')
        
class ScanAnalyze(Preview):
    
    extracted_data=ObjectProperty(None)
    
    @deco
    def analyze_pixels_callback(self, pixels, image_size, image_pos, scale, mirror):
        
        pimage=Image.frombytes(mode='RGBA',size=image_size,data=pixels)
        
        list_of_all_barcodes=decode(pimage)
        
        if list_of_all_barcodes:
           
            if self.extracted_data:
     
                self.extracted_data(list_of_all_barcodes[0])
        
class QrScreen(MDScreen):
    
    text_qr=''
    
    @deco
    def clear_qr_text(self,):
        
        sleep(5)
        
        self.text_qr= ''

    @mainthread    
    def focus(self,):
        
        self.parent.stop_progres(self)
        
        self.ids.scan.connect_camera(enable_analyze_pixels = True ,default_zoom=0.0)
    
    
    @deco
    def on_focus(self,):
        
        sleep(.5)
        
        self.focus()   
                       
    def get_qr_dialog(self,):  
        
        self.qr_card= QrDialog()
        
        if self.parent.user.id_user != {}:
                            
            if self.text_qr != '':

                self.qr_result()  
    
    @deco
    def qr_result(self,):
        
        try:

            route= self.parent.user.view_road(self.text_qr)
            
            if route != 'Error!':
            
                self.qr_card.text_card(route, self.parent.user)
                
                self.qr_card.qr_open()
                
                self.clear_qr_text()
            
            else:
                
                self.qr_card.text_card(dict(qr= self.text_qr, msj= 'Qr Invalido'), self.parent.user)
                
                self.qr_card.qr_open()
                
                self.clear_qr_text()
             
        except:
            
            self.parent.go_snack('Error de conexión')
            
            self.clear_qr_text()
            
    def close_cam(self,):
        
        try:
            
            self.enable_analyze_pixels = False 
            
            self.ids.scan.disconnect_camera()
            
        except:
            
            pass
     
    def check_printer(self,):
        
        passwd, ip, port= self.text_qr.split('|')
        
        self.parent.user.ip= ip
        
        self.parent.user.port= port
        
        self.parent.user.passwd= passwd
        
    @mainthread
    def got_result(self, result):
        
        if self.text_qr != result.data.decode('utf-8'):
            
            self.text_qr = result.data.decode('utf-8')
            
            if '|' in self.text_qr:
                
                self.check_printer()
                
                self.close_cam()
                
                self.parent.current= 'qrprinter' 
                
                self.parent.children[0].get_prepared()
                                  
            else:

                self.get_qr_dialog()
