import socket


class Client():
    
    def conect(self,):
        
        self.ip= input('ip ')
        
        self.port= int(input('port '))
        
        self.client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.client.connect((self.ip, self.port))

    def send(self,):
        
        msj= input('mjs')
        
        self.client.send(msj.encode())    
        
        
        
client= Client()

client.conect()

client.send()

client.send()

client.send()

client.client.close()