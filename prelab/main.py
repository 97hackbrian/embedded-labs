###MODULOS###
import serial,time
from tkinter import *
from PIL import Image,ImageTk,ImageSequence
from img.wmain import *
#############

###variables globales####


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


#region Window
######### CONFIGURACIÓN DE LA VENTANA PRINCIPAL #################

if __name__ == '__main__':
    start=window()
    #buyed=button()
    #buyed.position(100,100)
#endregion Window