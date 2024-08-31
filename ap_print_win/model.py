import socket
from PIL import Image, ImageWin
from uuid import uuid4
import win32print
import segno 
import win32con
import win32ui 
import json



class Printer():
    
    HORZRES = 8
    VERTRES = 10

    LOGPIXELSX = 88
    LOGPIXELSY = 90

    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 110

    PHYSICALOFFSETX = 12
    PHYSICALOFFSETY = 13
    
    PRINTER_QR= win32print.GetDefaultPrinter()
    
    PRINTER_TEXT= win32print.GetDefaultPrinter()

    def get_printers(self,):
        
        printers= win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL,None, 1)
        
        return printers
    
    def set_printers(self, printer):
        
        self.PRINTER_QR = printer
        
        self.PRINTER_TEXT= win32print.OpenPrinter(printer)
        
    def print_text(self, data):
      
      try:
        win32print.StartDocPrinter (self.PRINTER_TEXT, 1, ('Hoja de Ruta', None, "RAW"))
        
        try:
          win32print.StartPagePrinter (self.PRINTER_TEXT)
          win32print.WritePrinter (self.PRINTER_TEXT, bytes(data, "utf-8"))
          win32print.EndPagePrinter (self.PRINTER_TEXT)
        
        finally:
          win32print.EndDocPrinter (self.PRINTER_TEXT)
      
      finally:
        win32print.ClosePrinter (self.PRINTER_TEXT)
        
    def print_qr(self):

        file_name = "qr_id.png"


        hDC = win32ui.CreateDC ()
        hDC.CreatePrinterDC (self.PRINTER_QR.title())
        printable_area = hDC.GetDeviceCaps (self.HORZRES), hDC.GetDeviceCaps (self.VERTRES)
        printer_size = hDC.GetDeviceCaps (self.PHYSICALWIDTH), hDC.GetDeviceCaps (self.PHYSICALHEIGHT)
        printer_margins = hDC.GetDeviceCaps (self.PHYSICALOFFSETX), hDC.GetDeviceCaps (self.PHYSICALOFFSETY)

        bmp = Image.open (file_name)
        if bmp.size[0] > bmp.size[1]:
            bmp = bmp.rotate (90)

        ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
        scale = min (ratios)


        hDC.StartDoc (file_name)
        hDC.StartPage ()

        dib = ImageWin.Dib (bmp)
        scaled_width, scaled_height = [int (scale * i) for i in bmp.size]
        x1 = int ((printer_size[0] - scaled_width) / 2)
        y1 = int ((printer_size[1] - scaled_height) / 2)
        x2 = x1 + scaled_width
        y2 = y1 + scaled_height
        dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))

        hDC.EndPage ()
        hDC.EndDoc ()
        hDC.DeleteDC ()

class Qr():
    
    def qr_save(self, qr, name):

        self.qr= segno.make_qr(qr)
        
        self.qr.save( name , scale=3 )

class Conexion():

    server=  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
    HOST= socket.gethostbyname(socket.gethostname())
    
    PORT= 14532
    
    server.bind(( HOST , PORT))
    
    server.listen()
    
class SrvPrinter(Conexion, Qr, Printer):
    
    stop = False
    
    def stop_receive(self,):
        
        self.stop= True
        
        client_c= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        client_c.connect((self.HOST, self.PORT))
        
        client_c.recv(1024).decode()
        
        client_c.send(''.encode())
    
    def receive(self,):
        
        while True:
            
            if self.stop == True:
                
                break 

            self.client, self.address = self.server.accept()
            
            printers = self.get_printers()
            
            msj= json.dumps(printers)
        
            self.client.send(msj.encode())
            
            data = self.client.recv(2048).decode()
           
            data= json.loads(data)
            
            print(data)
            
            if data['password'] == str(self.password_new):
                
                self.set_printers(data['printer'])
                                
                self.qr_save(data['id'], 'qr_id.png') 
                
                self.print_text(data['text'])
                
                self.print_qr()
                
                self.client.close()
            
            else:
                            
                self.client.close()               
        
    def password(self,):
        
        self.password_new = uuid4()
        
        str_qr= str(self.password_new) + '|' + self.HOST + '|' + str(self.PORT)
        
        print(str_qr)
                        
        self.qr_save(str_qr, 'qr_conect.png')        

