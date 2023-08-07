###MODULOS###
import serial,time
from tkinter import *
import numpy as np
from PIL import Image,ImageTk,ImageSequence
from img.wmain import *
##############################################

###variables globales####
deal=np.array([0,0,0])



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


              
    
#region Window
######### CONFIGURACIÓN DE LA VENTANA PRINCIPAL #################

if __name__ == '__main__':
    root=Tk()
    start=window(parent=root)
    product1=products("zapato",130,root)
    #product2=products("pantalon",190,start)
    #product3=products("camisa",320,start)
    
    '''
    start.buttons("añadir",100,100)
    start.buttons("añadir",200,100)
    start.buttons("añadir",300,100)
    start.buttons("añadir",400,100)
    '''
    product1.show(400,300)
    #product2.show(400,400)
    #product3.show(400,500)
    ##products(start,3)


    #root.mainloop()
    start.refresh()
    
    
#endregion Window