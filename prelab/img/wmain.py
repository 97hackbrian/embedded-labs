from tkinter import *
import tkinter.font as tkFont
from img.wpopup import *
import numpy as np
import serial
import time
array=np.array([0,0,0,0])
np.savetxt("prelab/cart.txt", array)

try:
    ard=serial.Serial("/dev/ttyUSB0",9600)
    print("Connected")
except:
    print("Error to connect")

class window:
    global array
    def __init__(self,sizeW):
        self.window = Tk()
        self.window.geometry(sizeW)
        self.window.title("main")
        self.window['bg'] = '#F6F4EB'    
        self.labelf = tkFont.Font(family="graduation", size=60, weight="bold",slant="italic")

        self.label = Label(self.window, text="Bear Store DB", bg='#F6F4EB',fg='#4682A9')
        self.label.config(font=self.labelf)
        self.label.pack(anchor=CENTER)

        photocomp1=self.CreateImg("prelab/img/led.png",25,180)
        photocomp2=self.CreateImg("prelab/img/motor.png",25,250)
        photocomp3=self.CreateImg("prelab/img/rele.png",25,150)
        photocomp4=self.CreateImg("prelab/img/servo.png",25,130)



        self.product1=products("Led",0.5,photocomp1,self.window)
        self.product2=products("Motor",25,photocomp2,self.window)
        self.product3=products("Rele",35,photocomp3,self.window)
        self.product4=products("Servo",80,photocomp4,self.window)
        self.product1.show(250,150)
        self.product2.show(250,250)
        self.product3.show(250,350)
        self.product4.show(250,450)
        
      
        car = self.CreateImg("prelab/img/carrito.png",25,150)
        boton = Button(self.window,image=car,command=self.InitPopUp)
        boton.place(x=680, y=20)
        



        self.window.mainloop()

        

    def InitPopUp(self):
        self.product1.reset()
        self.product2.reset()
        self.product3.reset()
        self.product4.reset()
        Rei=popup()
        Pop=popup()
        #Pop.refresh()
    
    def CreateImg(self,dir,z,s):
        photocomp=PhotoImage(file=dir)
        photocomp = photocomp.zoom(z)
        photocomp = photocomp.subsample(s)
        return photocomp


    def exitmain(self):
        self.window.destroy()
    





class products:
    global array
    def __init__(self,n,p,img,win):
        self.d=0
        self.Text = tkFont.Font(family="GistLight", size=10, weight="bold",slant="italic")
        self.T = tkFont.Font(family="Garamond", size=12, weight="normal",slant="roman")
        self.Te = tkFont.Font(family="Garamond", size=12, weight="bold",slant="roman")

        self.wind=win
        self.name=n
        self.prize=p
        self.nameDisp=Label(win,text=n,bg='#F6F4EB')
        self.prizeDisp=Label(win,text=p,bg='#F6F4EB')
        self.addB=Button(win,text="Add",command=self.sum,bg='#749BC2',fg='#FFFFFF')
        
        self.lessB=Button(win,text="Remove",command=self.res,bg='#749BC2',fg='#FFFFFF')
        
        self.countDisp=Label(self.wind,text=self.d,bg='#F6F4EB')

        self.Cname=Label(win,text="Product name",bg='#F6F4EB')
        self.Cprize=Label(win,text="Prize of product",bg='#F6F4EB')
        self.Cquantity=Label(win,text="Quantity",bg='#F6F4EB')

        self.Try=Button(win,text="Try Componet",command=self.uart,bg='#91C8E4')
        

        self.nameDisp.config(font=self.T)
        self.prizeDisp.config(font=self.T)
        self.countDisp.config(font=self.T)

        self.addB.config(font=self.Te)
        self.lessB.config(font=self.Te)
        self.Try.config(font=self.Te)

        self.Cname.config(font=self.Text)
        self.Cprize.config(font=self.Text)
        self.Cquantity.config(font=self.Text)
        
        self.file_name = "prelab/cart.txt"
        self.f=array

        self.component = Label(win,image=img)
        

        
    def uart(self):
        global ard
        try:
            #ard=serial.Serial("COM6",9600)
            print("CONEXION CORRECTA")
            print("arduino ",self.name)
            if(self.name=="Led"):
                ard.write('1'.encode())
            elif(self.name=="Motor"):
                 ard.write('2'.encode())
            elif(self.name=="Rele"):
                 ard.write('3'.encode())
            elif(self.name=="Servo"):
                 ard.write('4'.encode())
            
            

        except:
            print("NO SE PUDO CONECTAR")


        
        

    def sum(self):
        
        self.d=self.d+1

        self.txt()
        np.savetxt(self.file_name, self.f)


        self.countDisp.configure(text=self.d)
        self.wind.update()
    def res(self):
        
        if(not self.d==0):
            self.d=self.d-1

            self.txt()
            np.savetxt(self.file_name, self.f)

            self.countDisp.configure(text=self.d)
            self.wind.update()
    
    def reset(self):
        self.d=0
        self.f=array
        self.txt()
        self.countDisp.configure(text=self.d)
        self.wind.update()
    
    def txt(self):
        if(self.name=="Led"):
            self.f[0]=self.d
        if(self.name=="Motor"):
            self.f[1]=self.d
        if(self.name=="Rele"):
            self.f[2]=self.d
        if(self.name=="Servo"):
            self.f[3]=self.d


    def show(self,x1,y1):
        self.Cname.place(x=x1-120,y=y1-30)
        self.nameDisp.place(x=x1-80,y=y1)
        self.Cprize.place(x=x1+2,y=y1-30)
        self.prizeDisp.place(x=x1+47,y=y1)
        self.addB.place(x=x1+150,y=y1)
        self.lessB.place(x=x1+280,y=y1)
        self.Try.place(x=x1+390,y=y1)
       
        self.Cquantity.place(x=x1+210,y=y1-30)
        self.countDisp.place(x=x1+235,y=y1)

        self.component.place(x=x1-230, y=y1-30)

        self.wind.update()