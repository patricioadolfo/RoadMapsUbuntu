from model import SrvPrinter
from kivymd.app import MDApp
from kivy.lang import Builder
import threading



class AppPrinter(MDApp):
    
    def on_stop(self):

        self.srv.stop_receive()
    


    def build(self,):
        
        self.srv= SrvPrinter()
        
        self.srv.password()
        
        threading.Thread(target= self.srv.receive).start()

        return Builder.load_file('kv.kv')
    
AppPrinter().run()