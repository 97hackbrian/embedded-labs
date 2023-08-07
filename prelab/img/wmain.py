from tkinter import *
import tkinter.font as tkFont


class window:
    
    def __init__(self,parent=None):
        self.window = parent
        self.window.geometry("700x600")
        self.window.title("main")
        self.window['bg'] = '#F6F4EB'    
          

        
        self.label = Label(parent, text="¡Bear Store DB!", bg='#F6F4EB',fg='#4682A9')
        self.label.pack(anchor=CENTER)
        self.labelf = tkFont.Font(family="Comic Sans MS", size=100, weight="bold",slant="italic",font=("Segoe Script", 35,'bold'))
        self.label.config(font=self.labelf)
        
        
        car = PhotoImage(file="prelab/img/carrito.png")
        car = car.zoom(25)
        car = car.subsample(150)
        boton = Button(image=car)
        boton.place(x=580, y=480)

        parent.mainloop()

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
        
        self.lessB=Button(win,text="remove",command=self.res)
        self.d=0
        self.countDisp=Label(self.wind,text=self.d)


        self.Cname=Label(win,text="Product name")
        self.Cprize=Label(win,text="Prize of product")
        self.Cquantity=Label(win,text="Quantity")

        self.Try=Button(win,text="TRY componet",command=self.uart)
        self.wind.update()
        

        
    def uart(self):
        pass
        

    def sum(self):
        self.d=self.d+1
        print("func: ",self.d)
        self.countDisp.configure(text=self.d)
        self.wind.update()
    def res(self):
        if(not self.d==0):
            self.d=self.d-1
            print("func: ",self.d)
            self.countDisp.configure(text=self.d)
            self.wind.update()
        
        
        

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
       
        self.Cquantity.place(x=x1+218,y=y1-30)
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
