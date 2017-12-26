'''
Created on Dec 25, 2017

@author: gustavo
'''
from gui.Plotter2D import Plotter2D
import tkinter as tk

main = tk.Tk()
main.wm_title("Legs State Plotter")
# Code to add widgets will go here...
p = Plotter2D(main).pack()

def subscriber_cb():
    



tk.mainloop()