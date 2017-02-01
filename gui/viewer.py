'''
Created on Jan 16, 2017

@author: gustavo
'''
import tkinter as tk
import matplotlib.image as mpimg
from matplotlib.figure import Figure
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
        self.roi = None
        self.loop = False        
        self.fig = Figure(figsize=(30/3,22.5/3))
        #ax = fig.add_subplot(111, projection='polar')
        self.ax = self.fig.add_subplot(111)
         
        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.fixed_lines = 0
        self.total_lines = 0
        
    def draw_img(self, img_path, limits=None):
        img = mpimg.imread(img_path)
        imgplot = self.ax.imshow(img, aspect='auto', extent=limits)
        self.__fit_to_roi()
        self.canvas.show()
        
        
    def __fit_to_roi(self):
        if self.roi != None:
            self.ax.set_ylim(ymin=self.roi["ymin"],ymax=self.roi["ymax"])
            self.ax.set_xlim(xmin=self.roi["xmin"],xmax=self.roi["xmax"])    
        
     
    def set_roi(self, roi): 
        self.roi = roi
     
    def plot(self, *args, **kwargs):
        self.ax.plot(*args, **kwargs)
        self.__fit_to_roi()
        self.canvas.show()
            
    def save_background(self):
        self.__fit_to_roi()
        self.canvas.show()
        self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)
        self.plot_data_tup = self.ax.plot(0, 0, 'b. ')
        print("tuple")
        print(self.plot_data_tup)
        self.cur_lines = len(self.plot_data_tup)
        self.plot_data = self.plot_data_tup[0]
        self.canvas.show()
        self.fixed_lines = len(self.ax.get_lines())
    
    def update_plot_data(self, *args, line_idx=0):
        
        print(self.plot_data)
        print(self.ax.get_lines())
        curr_line = self.plot_data_tup[line_idx]
        curr_line.set_data(*args)
        self.ax.draw_artist(curr_line)
        self.canvas.draw()
        return self.plot_data
                

if __name__ == "__main__":
    main = tk.Tk()
    main.wm_title("IMS Viewer")
    # Code to add widgets will go here...
    Viewer(main).pack()#(side="top", fill="both", expand="True")
    
    tk.mainloop()
        