from tkinter import *
import numpy as np
arrayR=np.array([0,0,0,0])
class popup:
    instancia = None
    window=None
    def __init__(self):
        pass
        #global arrayR
        #arrayR = np.loadtxt('prelab/cart.txt')
        #print(arrayR)
    def __new__(cls):
        global window
        global arrayR
        arrayR = np.loadtxt('prelab/cart.txt')
        cls.new=arrayR
        #print(arrayR)

        if cls.instancia is None:
            cls.instancia = super().__new__(cls)
            window=Tk()
            
            window.geometry("200x600")
            window.title("PopUp")
            window['bg'] = '#91C8E4'
            #print(window.winfo_exists())

            Title=Label(window,text="Cart",bg="#F6F4EB")
            Title.pack(anchor=CENTER)

            #print(cls.new)
            p1=Label(window,text=str(arrayR[0]),bg="#F6F4EB")
            p2=Label(window,text=str(arrayR[1]),bg="#F6F4EB")
            p3=Label(window,text=str(arrayR[2]),bg="#F6F4EB")
            p4=Label(window,text=str(arrayR[3]),bg="#F6F4EB")

            if(arrayR[0]>0):
                p1.pack(anchor="center")
            if(arrayR[1]>0):
                p2.pack(anchor="center")
            if(arrayR[2]>0):
                p3.pack(anchor="center")
            if(arrayR[3]>0):
                p4.pack(anchor="center")

            window.update()
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