from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationItem
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.clock import mainthread
from android_permissions import AndroidPermissions
import models   
from time import sleep

class Progress(MDFloatLayout):
    pass

class Snack(MDSnackbar):
    pass

class BaseMDNavigationItem(MDNavigationItem):
    
    icon = StringProperty()
    text = StringProperty()
 
class RmScreenManager(MDScreenManager):

    @mainthread
    def login_out_btn(self, btns):

        for btn in btns:

            btn.disabled= True

    @models.deco
    def login_out(self, log, btns):
        
        if log.icon != 'account-circle-outline': 
            
            self.user.logOut()

            self.event.cancel()
            
            log.icon= 'account-circle-outline'

            self.login_out_btn(btns)
            
    @mainthread
    def change_screen(self, screen):

        self.current= screen

    @models.deco
    def len_list(self, screen):

        while True:

            print(len(self.len_lists))

            if False in self.len_lists:

                self.stop_progres(self.get_screen(self.pre_screen))

                self.go_snack(self.msj)

                break


            if len(self.len_lists) == len(self.list):

                if not False in self.len_lists:

                    self.change_screen(screen)

                    self.stop_progres(self.get_screen(self.pre_screen))

                    break

            sleep(0.1)

    @models.deco
    def hilo(self,funcion):
            
        while True:

            if funcion.is_alive() == False:

                self.len_lists.append(True)

                break
                
            sleep(0.1)

    def go_screen(self, screen, list, msj):

        self.list = list

        self.len_lists = []

        self.pre_screen = self.current

        self.msj = msj

        for funcion in list:

            funcion= funcion

            self.hilo(funcion)

        self.len_list(screen)

    @mainthread 
    def go_snack(self, mnj):
        
        self.snack= Snack()
        
        self.snack.ids.snack_text.text= mnj
        
        self.snack.open()

    @mainthread
    def progress(self,screen):
        
        self.progres= Progress()
        
        screen.add_widget(self.progres)  
    
    @mainthread    
    def stop_progres(self, screen):
            
        screen.remove_widget(self.progres)

    user= models.User()

    event= ''

class RoadMapsApp(MDApp):
    
    icon= 'icons/truck.png'

    def on_start(self):
        
        self.dont_gc = AndroidPermissions(self.start_app)

    def start_app(self):
        
        self.dont_gc = None
        
    def load_log(self,):

        self.store = JsonStore('load.json')
        
        try:
        
            self.user = self.store.get('log')['name']   
            
            self.passwd= self.store.get('log')['pswd']
            
        except:
            
            self.user = ''   
            
            self.passwd= ''
        
        try:
            
            self.ip= self.store.get('url')['ip']
        
        except:    
            
                self.ip= ''
    
    def on_checkbox_active(self, checkbox, value):

        if value:
    
            self.root.ids.screen_manager.user.printer= checkbox.parent.parent.children[1].children[0].children[0].text    

            self.store.put('print', print= self.root.ids.screen_manager.user.printer )
    
    def build(self):
        
        self.set_bars_colors()

        self.theme_cls.primary_hue = "A700"
       
        self.theme_cls.theme_style = "Dark"  

        self.theme_cls.primaryColor= [0.08232529, 0.0745098, 0.521569, 1.0]  

        self.theme_cls.tercearyColor= [0.913725, 0.501961, 0.137255, 1.0]
        
        self.load_log()
 
        return Builder.load_file('kv.kv')
                
    def set_bars_colors(self):
        
        set_bars_colors(
            [0.08232529, 0.0745098, 0.521569, 1.0] ,  # status bar color
            [0.08232529, 0.0745098, 0.521569, 1.0],  # navigation bar color
            "Light",      # icons color of status bar
        )
    
if __name__ == "__main__":
    
    RoadMapsApp().run()