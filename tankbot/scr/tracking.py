from time import sleep
import sys
sys.path.append('/root/Desktop/embedded-labs/tankbot')
#sys.path.append('/home/hackbrian/Documentos/gitProyects/embedded-labs/tankbot')
from libs.tiva import *
from libs.pixie import *
size_camera=500
if __name__ == "__main__":
    camara=Camara(max_attempts=5)
    tiva=InitSerial(baud=9600)
    motors=Motors(serial_instance=tiva)
    leds=LedControl(serial_instance=tiva)
    leds.init_system(cam=1)
    pos=[]
    while True:
        
        pos,ref=camara.track()
        posx=pos[0]
        posy=pos[1]
        print("x: ",posx,"  y: ",posy,"  ref: ",ref)
        if ref==1:
            if(posx<=size_camera/2)+50:
                motors.move(-60,60)
            elif((posx>=(size_camera/2)-50) and (posx<=(size_camera/2)+50)):
                motors.stop()
            elif(posx>=size_camera/2)-50:
                motors.move(60,-60)
        else:
            motors.stop()
