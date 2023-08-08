from tkinter import *
import tkinter.font as tkFont
from img.wpopup import *
import numpy as np

array=np.array([0,0,0,0])
np.savetxt("cart.txt", array)
class window:
    global array
    def __init__(self,parent=None):
        self.window = parent
        self.window.geometry("800x600")
        self.window.title("main")
        self.window['bg'] = '#F6F4EB'    
          

        
        self.label = Label(parent, text="Bear Store DB", bg='#F6F4EB',fg='#4682A9')
        self.label.pack(anchor=CENTER)
        self.labelf = tkFont.Font(family="graduation", size=60, weight="bold",slant="italic")
        self.label.config(font=self.labelf)
        
        
        self.file_name = "cart.txt"
        self.dat=array
        parent.update()

        

    def refresh(self):
        car = PhotoImage(file="prelab/img/carrito.png")
        car = car.zoom(25)
        car = car.subsample(150)
        boton = Button(self.window,image=car,command=self.InitPopUp)
        boton.place(x=680, y=20)
        #np.savetxt(self.file_name, self.dat)
        self.window.mainloop()

    def InitPopUp(self):
        #np.savetxt(self.file_name, self.dat)
        Rei=popup()
        Pop=popup()
        #np.savetxt(self.file_name, self.dat)
        #Pop.refresh()
    
    def exitmain(self):
        self.window.destroy()
    





class products:
    global array
    def __init__(self,n,p,win):
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
        self.d=0
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

        
        self.file_name = "cart.txt"
        #np.savetxt(self.file_name,array)
        self.f=array
        self.wind.update()
        

        
    def uart(self):
        pass
        

    def sum(self):
        
        self.d=self.d+1
        print("func: ",self.d)
        self.txt()
        np.savetxt(self.file_name, self.f)
        #popup()

        self.countDisp.configure(text=self.d)
        self.wind.update()
    def res(self):
        
        if(not self.d==0):
            self.d=self.d-1
            print("func: ",self.d)
            self.txt()
            np.savetxt(self.file_name, self.f)
            #popup()

            self.countDisp.configure(text=self.d)
            self.wind.update()
    
    def get_instance_name(self):
        for name, obj in globals().items():
            if obj is self:
                return name
        return None
    
    def txt(self):
        #with open(self.file_name, 'a') as f:
        if(self.name=="Led"):
            self.f[0]=self.d
        if(self.name=="Motor"):
            self.f[1]=self.d
        if(self.name=="Rele"):
            self.f[2]=self.d
        if(self.name=="Servo"):
            self.f[3]=self.d
        #np.savetxt(self.file_name, self.f)

    
        

    def show(self,x1,y1):
        self.Cname.place(x=x1-120,y=y1-30)
        self.nameDisp.place(x=x1-95,y=y1)
        self.Cprize.place(x=x1-7,y=y1-30)
        self.prizeDisp.place(x=x1+25,y=y1)
        #self.addB.position(x+10,y,win,"add")
        self.addB.place(x=x1+150,y=y1)
        #self.lessB.position(x+120,y,win,"remove")
        self.lessB.place(x=x1+280,y=y1)
        #print(obj.quanty(self.d))
        self.Try.place(x=x1+390,y=y1)
        
        print("disp: ",self.d)
       
        self.Cquantity.place(x=x1+210,y=y1-30)
        self.countDisp.place(x=x1+235,y=y1)

        
        self.wind.update()
    

    





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
