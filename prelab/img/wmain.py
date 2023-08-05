from tkinter import *
#from tkinter import ttk

class window:
    
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1200x700")
        self.window.title("main")
        self.window['bg'] = '#F133FF'
        #buy=button(self.window,"lol").position(100,100)
        
    def buttons(self,msg,posx,posy):
        button(self.window,msg).position(posx,posy)
    def refresh(self):
        self.window.mainloop()
    def exitmain(self):
        self.window.destroy()
    
class button:
    def __init__(self,win,tex):
        self.buy=Button(win,text=tex)
    def position(self,x1,y1):
        self.buy.place(x=x1,y=y1)
