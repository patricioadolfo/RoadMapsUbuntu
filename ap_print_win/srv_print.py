from time import sleep

import socket
import threading
import win32timezone



class Conexion:

    server=  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    HOST= socket.gethostbyname(socket.gethostname())
    print(HOST)
    
    PORT= 14532

    server.bind(("localhost", PORT))
    server.listen()
    

    
class Servidor(Conexion):


    def receive(self, printer, timer):
        
        while True:
            
            client, address = self.server.accept()
            
            print(address)
            
            tread_print= threading.Thread(target= self.print_job, args=(client, printer, timer,))
            tread_print.start()
              
    def send_job(self, client, mensj):
                        
            try: 
                client.send(mensj.encode())
            
            except:
                client.close()
  
    def print_job(self, client, printer, timer):
        
        comanda= []
        
        while True:
            
            jobs= win32print.EnumJobs(printer, 0, -1, 1)
            
            for job in jobs:
                
                if job['JobId'] in comanda:
                    pass
                    
                else:
                    try:
                        self.send_job(client, job['pMachineName'])
                        
                        comanda.append(job['JobId'])
                
                    except:
                        client.close()
                        break
            
            if len(comanda) > 50:
                comanda= []
            
            sleep(timer)


        
  

if __name__ == "__main__":
    
    a= Servidor()
    
    
    #printer= win32print.OpenPrinter(dato[0])
    
    #a.receive(printer, float(dato[1]))



# para .exe
# py -3.10 -m PyInstaller --paths C:\Users\Patricio\AppData\Roaming\Python\Python310\site-packages\pywin32_system32  --onefile main.py