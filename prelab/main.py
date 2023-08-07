###MODULOS###
import serial,time
from tkinter import *
from PIL import Image,ImageTk,ImageSequence
from img.wmain import *
##############################################

###variables globales####
deal=[0,0,0]
deal = list(map(int, deal))


#region Serial
'''
########## CONEXION MEDIANTE EL PROTOCOLO SERIAL ###############
try:
        ard=serial.Serial("/dev/ttyUSB0",2000000,timeout=5);
        print("CONEXION CORRECTA")
        mensaje='ARDUINO CONECTADO'
        
        

except:
        print("NO SE PUDO CONECTAR")
        mensaje='ARDUINO NO CONECTADO'
###############################################################
#endregion Serial
'''
'''
def products(obj,n):
    for x in range(n):
        obj.buttons(x+1,100,100*x)
'''

class products:
        global deal
        def __init__(self,n,d,p):
               self.name=n
               self.prize=p
               self.sum=int(d)
               print(self.prize)
        def show(self,obj,x,y):
              obj.label(self.name,x-120,y)
              obj.label(self.prize,x-40,y)
              
              obj.buttons("add",x+10,y,self.sum)
              self.sum=obj.buttons("remove",x+120,y,self.sum)
              obj.label(self.sum,x+80,y)
              
    
#region Window
######### CONFIGURACIÓN DE LA VENTANA PRINCIPAL #################

if __name__ == '__main__':
    start=window()
    product1=products("zapato",int(deal[0]),130)
    product2=products("pantalon",deal[1],190)
    product3=products("camisa",deal[2],320)
    '''
    start.buttons("añadir",100,100)
    start.buttons("añadir",200,100)
    start.buttons("añadir",300,100)
    start.buttons("añadir",400,100)
    '''
    product1.show(start,400,300)
    product2.show(start,400,400)
    product3.show(start,400,500)
    ##products(start,3)

    start.refresh()
    
    
#endregion Window