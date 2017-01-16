'''
Created on Jan 16, 2017

@author: gustavo
'''
import threading
import time
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Viewer(tk.Frame):
    '''
    classdocs
    '''    
    def __init__(self, master):
        '''
        Constructor
        '''        
        tk.Frame.__init__(self, master)
        
        self.master = master        
        self.loop = False        
        self.fig = plt.figure(figsize=(30/3,22.5/3))
        #ax = fig.add_subplot(111, projection='polar')
        self.ax = self.fig.add_subplot(111)
         
        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # tk.Frame.__init__(self, master)
        
        button_frame = tk.Frame(self)
        nbutton = tk.Button(button_frame, text="Next",
                           command=self._next_frame)
        nbutton.pack(side="left")
        lbutton = tk.Button(button_frame, text="Loop",
                           command=self._loop)
        lbutton.pack(side="left")
        sbutton = tk.Button(button_frame, text="Stop",
                           command=self._stop)
        sbutton.pack(side="left")
        button_frame.pack(side="top")
        
        self.new_data_cb = None
        self.ts = 0
        
        
        
    def _loop(self):
        self.loop = True
        t1 = threading.Thread(target=self._loop_thread)
        t1.start()
        
        
            
    def _loop_thread(self):
        while self.loop:
            last_ts = self.ts
            print("clear")
            data, last, self.ts = self.new_data_cb()
            diff = self.ts - last_ts
            time.sleep(diff/1000.0)
            self.plot_data.set_data(data[:,0], data[:,1])
            self.ax.draw_artist(self.plot_data)
            self.canvas.show()     
    
    def _stop(self):
        self.loop = False
        
    def _next_frame(self):
        #self.ax.clear()
        #self.canvas.show()
        print("clear")
        data, last, self.ts = self.new_data_cb()
        self.plot_data.set_data(data[:,0], data[:,1])
        self.ax.draw_artist(self.plot_data)
        self.canvas.show()

if __name__ == "__main__":
    main = tk.Tk()
    main.wm_title("IMS Viewer")
    # Code to add widgets will go here...
    Viewer(main).pack()#(side="top", fill="both", expand="True")
    
    tk.mainloop()
        