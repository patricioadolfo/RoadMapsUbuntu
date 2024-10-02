from camera4kivy import Preview
from PIL import Image
from pyzbar.pyzbar import decode
from kivy.clock import mainthread
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from time import sleep
from models import deco

        
class ScanAnalyze(Preview):
    
    extracted_data=ObjectProperty(None)
    
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

        self.manager.dialog_qr()

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
            
            if route != False:
            
                self.manager.dialog.text_card(route, self.manager)
                
                self.manager.dialog.qr_open()
            
            else:
                
                self.manage.dialog.text_card(dict(qr= self.text_qr, msj= 'Qr Invalido'), self.manager)
                
                self.manager.dialog.qr_open()

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
                
        if self.parent.user.id_user != {}:
                            
            if self.text_qr != '':

                self.manager.go_screen(self.manager.current, [self.qr_result()], 'Error de conexión')