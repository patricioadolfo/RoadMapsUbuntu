
from winotify import Notification, audio
import socket

def ini():
        
    with open("ini2.txt", "r") as conf:
        
        ip, sound = conf.read().split(";")
    
    conf.close()
    
    return ip , sound


class Cliente():
    
    def __init__(self, conf):
        
        self.ip= conf[0]
        self.sound= conf[1]
        
        PORT = 14532
               
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("localhost", PORT))
        

    def rec(self):
        
        while True:
            
            data= self.client.recv(1024).decode("utf-8")
            
            self.alert(data)
    
    def alert(self, job):
        
        notif = Notification(app_id="Windows app", 
                             title="Nueva Comanda",
                             msg=job,
                             duration="short"
                             )

        notif.set_audio(audio.Default, loop= False)
    

        notif.show()


if __name__ == "__main__":

    conf=ini()
    
    cliente= Cliente(conf)
    
    cliente.rec()




# para .exe
# py -3.10 -m PyInstaller --paths C:\Users\Patricio\AppData\Roaming\Python\Python310\site-packages\pywin32_system32  --onefile main.py