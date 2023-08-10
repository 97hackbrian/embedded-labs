###MODULOS###
#import serial,time
from tkinter import *
import numpy as np
from PIL import Image,ImageTk,ImageSequence
from img.wmain import *
##############################################

###variables globales####
deal=np.array([0,0,0])




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


              
    
#region Window
######### CONFIGURACIÓN DE LA VENTANA PRINCIPAL #################

if __name__ == '__main__':
    #root=Tk()


    start=window("800x600")
    
    '''
    product1=products("Led",0.5,root)
    product2=products("Motor",25,root)
    product3=products("Rele",35,root)
    product4=products("Servo",80,root)
    product1.show(250,150)
    product2.show(250,250)
    product3.show(250,350)
    product4.show(250,450)
    start.refresh()'''
    
    
#endregion Window