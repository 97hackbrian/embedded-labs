from tkinter import *
import tkinter.font as tkFont

#from tkinter import ttk

class window:
    
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1200x700")
        self.window.title("main")
        self.window['bg'] = '#F133FF'


    def buttons(self,msg,posx,posy,sum):
        button(self.window,msg,sum).position(posx,posy)
        return button(self.window,msg,sum)

    
    
    def label(self,msg,posx,posy):
        label().text(msg,self.window,posx,posy)
    def refresh(self):
        self.window.mainloop()
    def exitmain(self):
        self.window.destroy()
    
class button:
    def __init__(self,win,tex,val1):
        self.B=Button(win,text=tex,command=self.clicadd(val1))
    def clicadd(self,val):
        val=int(val)+1
        return int(val)
    def position(self,x1,y1):
        self.B.place(x=x1,y=y1)

class label:
    def __init__(self):
        self.Text = tkFont.Font(family="Comic Sans MS", size=12, weight="bold",slant="italic",font=("Segoe Script", 18,'bold'))
    def text(self,msg,win,x1,y1):
        self.Text=Label(win,text=msg)
        self.Text.place(x=x1,y=y1)

'''
class product:
    def __init__(self,obj,n,prize):
        self.win=
        self.n=n
        self.prize=prize
    def create(self):
        for x in range(self.n):
            self.win.bu(x,100*x,100)
'''            
