from tkinter import *
import tkinter.font as tkFont
import numpy as np
import datetime

import os
import sys
arrayR=np.array([0,0,0,0])
class popup:
    instancia = None
    window=None
    def __init__(self):
        pass
        #global arrayR
        #arrayR = np.loadtxt('prelab/cart.txt')
        #print(arrayR)
    
    
    
    def hist():
        global arrayR
        stp1=arrayR[0]*0.5
        stp2=arrayR[1]*25
        stp3=arrayR[2]*35
        stp4=arrayR[3]*80

        Time = datetime.datetime.now()
        File=open("cartHist.txt","at")
        File.write("\n\n\n\n"+str(Time)+"\n")
        if(arrayR[0]>0):
            File.write("\nLed:  quantity:"+str(arrayR[0])+"  SubTotal: "+str(arrayR[0]*0.5))
        if(arrayR[1]>0):
            File.write("\nMotor:  quantity:"+str(arrayR[1])+"  SubTotal: "+str(arrayR[1]*25))
        if(arrayR[2]>0):
            File.write("\nRele:  quantity:"+str(arrayR[2])+"  SubTotal: "+str(arrayR[2]*35))
        if(arrayR[3]>0):
            File.write("\nServo:  quantity:"+str(arrayR[3])+"  SubTotal: "+str(arrayR[3]*80))
        
        File.write("\n TOTAL: "+str(stp1+stp2+stp3+stp4)+" Bs.")
        
        window.destroy()
        sys.stdout.flush()
        os.execv(sys.argv[0], sys.argv)
    



    def __new__(cls):
        global window
        global arrayR
        arrayR = np.loadtxt('prelab/cart.txt')
        cls.new=arrayR
        #print(arrayR)
    
    
        

        if cls.instancia is None:
            cls.instancia = super().__new__(cls)
            window=Tk()
            
            window.geometry("450x600")
            window.title("PopUp")
            window['bg'] = '#91C8E4'
            #print(window.winfo_exists())

            labelf = tkFont.Font(family="graduation", size=70, weight="normal",slant="roman")

            Title=Label(window,text="Cart",bg="#91C8E4")
            Title.config(font=tkFont.Font(family="graduation", size=80, weight="bold",slant="italic"))
            Title.pack(anchor=CENTER,ipady="50")

            
            
            #print(cls.new)
            stp1=arrayR[0]*0.5
            stp2=arrayR[1]*25
            stp3=arrayR[2]*35
            stp4=arrayR[3]*80
            p1=Label(window,text="Led -  Quantity: "+str(arrayR[0])+"    Subtotal: "+str(stp1),bg="#91C8E4")
            p2=Label(window,text="Motor -  Quantity: "+str(arrayR[1])+"    Subtotal: "+str(stp2),bg="#91C8E4")
            p3=Label(window,text="Rele -  Quantity: "+str(arrayR[2])+"    Subtotal: "+str(stp3),bg="#91C8E4")
            p4=Label(window,text="Servo -  Quantity: "+str(arrayR[3])+"    Subtotal: "+str(stp4),bg="#91C8E4")
            p1.config(font=labelf)
            p2.config(font=labelf)
            p3.config(font=labelf)
            p4.config(font=labelf)
            if(arrayR[0]>0):
                p1.pack(ipady="10")
            if(arrayR[1]>0):
                p2.pack(ipady="10")
            if(arrayR[2]>0):
                p3.pack(ipady="10")
            if(arrayR[3]>0):
                p4.pack(ipady="10")

            Total=Label(window,text="TOTAL  "+str(stp1+stp2+stp3+stp4)+" Bs.",bg="#91C8E4")
            Total.config(font=labelf)
            Total.pack(fill="y",ipady="20")

            PurC=Button(window,text="PURCHASE",bg="#91C8E4",command=cls.hist)
            PurC.config(font=labelf)
            PurC.pack(side="bottom",anchor="center")

            #window.update()
            window.mainloop()
        else:
            print("no")
            try:
                if not window.winfo_exists():
                    cls.instancia=None
            except:
                print("test")
                cls.instancia=None
        return cls.instancia
    