import models   
from time import sleep
from kivy.clock import mainthread
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.storage.jsonstore import JsonStore
from dialogs.dialog import DialogIp, QrDialog, DialogCreate, HomeDialog

class Progress(MDFloatLayout):
    pass

class Snack(MDSnackbar):
    pass

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

    def dialog_order(self, branch):

        self.dialog= DialogCreate()

        self.dialog.open_dialog(self, branch)
    
    def open_ipdialog(self,):

        self.dialog= DialogIp()

        self.dialog.open_dilog(self.store)
    
    def dialog_qr(self,):

        self.dialog=  QrDialog()

    def dialog_home(self,):

        self.dialog= HomeDialog()

    @models.deco
    def go_cam(self,):

        sleep(.9)

        self.ids.qr_screen.on_focus()

        self.stop_progres(self.ids.qr_screen)

    user= models.User()

    store = JsonStore('load.json') 

    event= ''