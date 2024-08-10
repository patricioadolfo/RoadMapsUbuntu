import win32print
import win32ui
import win32con
from PIL import Image, ImageWin
 
INCH = 1440 
HORZRES = 8
VERTRES = 10
#
# LOGPIXELS = dots per inch
#
LOGPIXELSX = 88
LOGPIXELSY = 90
#
# PHYSICALWIDTH/HEIGHT = total area
#
PHYSICALWIDTH = 110
PHYSICALHEIGHT = 110
#
# PHYSICALOFFSETX/Y = left / top margin
#
PHYSICALOFFSETX = 12
PHYSICALOFFSETY = 13

printer_name = win32print.GetDefaultPrinter ()
file_name = "qr_id.png"

printer= win32print.OpenPrinter(printer_name)
# You can only write a Device-independent bitmap
#  directly to a Windows device context; therefore
#  we need (for ease) to use the Python Imaging
#  Library to manipulate the image.
#
# Create a device context from a named printer
#  and assess the printable size of the paper.

data= """

safsdf
sdf
sd
fsd
f
sdf
sd
f
"""
      
try:
  win32print.StartDocPrinter (printer, 1, ('Hoja de Ruta', None, "RAW"))
  
  try:
    win32print.StartPagePrinter (printer)
    win32print.WritePrinter (printer, bytes(data, "utf-8"))
    win32print.EndPagePrinter (printer)
  
  finally:
    win32print.EndDocPrinter (printer)

finally:
  win32print.ClosePrinter (printer)
#
hDC = win32ui.CreateDC ()
hDC.CreatePrinterDC (printer_name)
printable_area = hDC.GetDeviceCaps (HORZRES), hDC.GetDeviceCaps (VERTRES)
printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)
printer_margins = hDC.GetDeviceCaps (PHYSICALOFFSETX), hDC.GetDeviceCaps (PHYSICALOFFSETY)

#
# Open the image, rotate it if it's wider than
#  it is high, and work out how much to multiply
#  each pixel by to get it as big as possible on
#  the page without distorting.
#
bmp = Image.open (file_name)
if bmp.size[0] > bmp.size[1]:
  bmp = bmp.rotate (90)

ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
scale = min (ratios)

#
# Start the print job, and draw the bitmap to
#  the printer device at the scaled size.
#
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