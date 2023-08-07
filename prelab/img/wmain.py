from tkinter import *
import tkinter.font as tkFont

#from tkinter import ttk

class window:
    
    def __init__(self,parent=None):
        self.window = parent
        self.window.geometry("1200x700")
        self.window.title("main")
        self.window['bg'] = '#A307AF'



    def refresh(self):
        self.window.mainloop()
    
    def exitmain(self):
        self.window.destroy()
    





class products:
    def __init__(self,n,p,win):
        self.Text = tkFont.Font(family="Comic Sans MS", size=12, weight="bold",slant="italic",font=("Segoe Script", 18,'bold'))
        self.wind=win
        self.name=n
        self.prize=p
        self.nameDisp=Label(win,text=n)
        self.prizeDisp=Label(win,text=p)
        self.addB=Button(win,text="add",command=self.sum)
        
        self.lessB=Button(win,text="remove")
        self.d=0
        self.countDisp=Label(self.wind,text=self.d)
        

    def sum(self):
        self.d=self.d+1
        print(self.d)
        

    def show(self,x1,y1):
        self.nameDisp.place(x=x1-120,y=y1)
        self.prizeDisp.place(x=x1-40,y=y1)
        #self.addB.position(x+10,y,win,"add")
        self.addB.place(x=x1+10,y=y1)
        #self.lessB.position(x+120,y,win,"remove")
        self.lessB.place(x=x1+120,y=y1)
        #print(obj.quanty(self.d))
        
        self.countDisp.place(x=x1+80,y=y1)

    





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
