from tkinter import *
import numpy as np
import threading
arrayR=np.array([0,0,0,0])
#arrayR = np.loadtxt('cart.txt')

'''
def ReadTxt():
    while True:
        global arrayR
        arrayR = np.loadtxt('cart.txt')
        #print(arrayR)
        


hilo1 = threading.Thread(target=ReadTxt)
hilo1.start()
'''
class popup:
    
    instancia = None
    window=None
    def __init__(self):
        global arrayR
        arrayR = np.loadtxt('cart.txt')
        #print(arrayR)
        
        

    '''def ReadTxt(self):
        while True:
            global arrayR
            arrayR = np.loadtxt('cart.txt')
            #print(arrayR)

    hilo1 = threading.Thread(target=ReadTxt)
    hilo1.start()'''
    
    def __new__(cls):
        
        global window
        global arrayR
        arrayR = np.loadtxt('cart.txt')
        cls.new=arrayR
        #print(arrayR)
        
    

        if cls.instancia is None:
            cls.instancia = super().__new__(cls)
            window=Tk()
            
            '''
            if not window.winfo_exists():
                cls.instancia=None
            else:
                cls.instancia = super().__new__(cls)
                '''
                
            window.geometry("200x600")
            window.title("PopUp")
            window['bg'] = '#91C8E4'
            print(window.winfo_exists())


            Title=Label(window,text="Cart",bg="#F6F4EB")
            Title.pack(anchor=CENTER)

            print(cls.new)
            p1=Label(window,text=str(arrayR[0]),bg="#F6F4EB")
            p1.place(x=50,y=50)
            


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
        try:
            pass
        except:
            p1=Label(window,text=str(arrayR[0]),bg="#F6F4EB")
            p1.place(x=50,y=50)

        return cls.instancia
    

