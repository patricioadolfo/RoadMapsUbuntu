from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationItem
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy.storage.jsonstore import JsonStore

from android_permissions import AndroidPermissions


class BaseMDNavigationItem(MDNavigationItem):
    
    icon = StringProperty()
    text = StringProperty()

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