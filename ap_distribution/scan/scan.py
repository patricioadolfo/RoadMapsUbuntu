from kivy.properties import ObjectProperty
from camera4kivy import Preview
from PIL import Image
from pyzbar.pyzbar import decode
from kivy.clock import mainthread
from models import deco
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from time import sleep


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
            
            self.ids.origin_dialog.text= 'De '+ dict['origin_name']
            
            self.ids.destin_dialog.text=  'Para '+ dict['destination_name']
                                 
    @mainthread
    def close_card(self,):
        
        self.dismiss()      
                
    def status(self, dict):
        
        if 'status' in dict:
        
            if dict['status'] == 'p':
                
                self.ids.btn_rec.disabled= False
                
                detail_text= 'Envio n° {id}, preparado el dia {date} a las {time}'.format(
                                                                                        id= str(dict['id']),
                                                                                        date= dict['preparation_date'],
                                                                                        time= dict['preparation_time'],
                                                                                           ) 
            
            elif dict['status'] == 'c':
                
                detail_text= 'Envio n° {id} en camino'.format(id= str(dict['id']))
            
            else:
                
                detail_text= 'Envio n° {id} recibido'.format(id= str(dict['id']))
            
            return detail_text
        
        if 'qr' in dict:
            
            detail_text= dict['qr'] + '\n' + dict['msj']
            
            return detail_text
            
    @deco
    def receive_route(self):
        
        try:
    
            self.manager.user.on_road(str(self.dict['id']))
        
            self.close_card()
        
        except:
            
            self.manager.len_lists.append(False)
             
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
 
    def focus(self,dt):
        
        self.ids.scan.connect_camera(enable_analyze_pixels = True, enable_video = False)

    @deco
    def on_focus(self,):

        try:
            
            self.manager.user.clock.schedule_once(self.focus)

        except:

            self.manager.len_lists.append(False)
        
    @deco
    def qr_result(self,):
            
        try:

            route= self.manager.user.view_road(self.text_qr + '/')
            
            if route != 'Error!':
            
                self.qr_card.text_card(route, self.manager)
                
                self.qr_card.qr_open()
            
            else:
                
                self.qr_card.text_card(dict(qr= self.text_qr, msj= 'Qr Invalido'), self.manager)
                
                self.qr_card.qr_open()

        except:
            
            self.manager.len_lists.append(False)
            
        self.clear_qr_text()
      
    @mainthread
    def _close_cam(self,):

        self.ids.scan.disconnect_camera()
    
    @deco
    def close_cam(self,):
        
        try:
            
            self._close_cam()
 
        except:
            
            self.manager.len_lists.append(False)
        
    @mainthread
    def got_result(self, result):
        
        if self.text_qr != result.data.decode('utf-8'):
            
            self.text_qr = result.data.decode('utf-8')
                
            self.manager.progress(self)

            self.get_qr_dialog()

    def get_qr_dialog(self,):  
        
        self.qr_card= QrDialog()
        
        if self.parent.user.id_user != {}:
                            
            if self.text_qr != '':

                self.manager.go_screen(self.manager.current, [self.qr_result()], 'Error de conexión')


        
