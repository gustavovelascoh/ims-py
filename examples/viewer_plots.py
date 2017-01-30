'''
Created on Jan 29, 2017

@author: gustavo
'''
import tkinter as tk


class Multiplot(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        button_frame = tk.Frame(self)
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
        
    def plot_a(self):
        pass
    
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
    