from tkinter import *
#from tkinter import ttk
class window:
    
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1200x700")
        self.window.title("main")
        self.window['bg'] = '#F133FF'
        buy=button(self.window).position(100,100)
        self.window.mainloop()
    
    def exitmain(self):
        self.window.destroy()
    
class button():
    def __init__(self,w):
        self.buy=Button(w,text="hola")
    def position(self,x1,y1):
        self.buy.place(x=x1,y=y1)
    def 