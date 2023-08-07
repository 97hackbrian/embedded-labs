from tkinter import *
class popup:
    def __init__(self):
        self.window=Tk()
        self.window.geometry("200x300")
        self.window.title("PopUp")
        self.window['bg'] = '#91C8E4'    
    def refresh(self):
        self.window.mainloop()

