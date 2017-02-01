'''
Created on Jan 29, 2017

@author: gustavo
'''
import tkinter as tk
import sys
from numpy import arange, sin, pi


sys.path.append("..")

from gui.viewer import Viewer

class Multiplot(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        button_frame = tk.Frame(self)
        button_bg = tk.Button(button_frame, text="Plot BG",
                           command=self.plot_bg)
        button_bg.pack(side="left")
        button_a = tk.Button(button_frame, text="Plot A",
                           command=self.plot_a)
        button_a.pack(side="left")
        button_b = tk.Button(button_frame, text="Plot B",
                           command=self.plot_b)
        button_b.pack(side="left")
        button_c = tk.Button(button_frame, text="Plot C",
                           command=self.plot_c)
        button_c.pack(side="left")
        button_clr = tk.Button(button_frame, text="Clear",
                           command=self.plot_clr)
        button_clr.pack(side="left")
        button_frame.pack(side="top")
        
        
        
        self.viewer = Viewer(self)
        self.viewer.pack()
        
        roi={"ymin":-2,"ymax":2,"xmin":-10,"xmax":10}
        self.viewer.set_roi(roi)
        
    def plot_bg(self):
        self.viewer.canvas.show()
        self.viewer.save_background()
            
    def plot_a(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        
        self.viewer.update_plot_data(t,s)
        
            
    
    def plot_b(self):
        pass
    
    def plot_c(self):
        pass
    
    def plot_clr(self):
        pass

if __name__ == '__main__':
    main = tk.Tk()
    main.wm_title("Viewer example")
    m =Multiplot(main)
    m.pack(side="top", fill="both", expand="True")
    
    tk.mainloop()
    