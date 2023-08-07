from tkinter import *
class popup:



    instancia = None
    window=None
    def __init__(self):
        pass
    def __new__(cls):
        global window
        if cls.instancia is None:
            cls.instancia = super().__new__(cls)
            window=Tk()
            '''
            if not window.winfo_exists():
                cls.instancia=None
            else:
                cls.instancia = super().__new__(cls)
                '''
                
            window.geometry("200x300")
            window.title("PopUp")
            window['bg'] = '#91C8E4'
            print(window.winfo_exists())


        
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
    

