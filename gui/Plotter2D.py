'''
Created on Dec 25, 2017

@author: gustavo
'''
import tkinter as tk
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Plotter2D(tk.Frame):
    def __init__(self, master, cb=None):
        '''
        Constructor
        '''        
        tk.Frame.__init__(self, master)
        
        self.master = master
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
         
        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.total_lines = 0
        self.fixed_lines = 0
        self.used_lines = 0
        
    def plot(self, *args, **kwargs):
        self.available_lines = self.total_lines - self.fixed_lines - self.used_lines

        if self.available_lines > 0:
#             print("Updating line ")
            line_idx = (self.fixed_lines + self.used_lines)            
            self.__update_plot_data( *args, line_idx=line_idx)
            #self.update_style(line_idx, **kwargs)
            
        else:
            self.ax.plot(*args, **kwargs)            
            #self.update_style(line_idx="last", **kwargs)
            self.total_lines = len(self.ax.get_lines())
        
        self.used_lines += 1
    
    def __update_plot_data(self, *args, line_idx=0):
        
        #print(self.plot_data)
        list_of_lines = self.ax.get_lines()
        #print("Length lol %d" % len(list_of_lines))
        curr_line = list_of_lines[line_idx]
        if len(args) == 2:
            curr_line.set_data(*args)
        else:
            curr_line.set_data(*args[0:2])
            curr_line.set_linestyle(args[2])
            
        
        self.ax.draw_artist(curr_line)  
    
    def update(self, xmin=None, xmax=None):
        
        
        lines_to_discard = self.total_lines - self.fixed_lines - self.used_lines
        #print("l2d: %d", lines_to_discard)
        
        lines = self.ax.get_lines()
        #print("Length lol %d" % len(lines))
        for i in range(0,lines_to_discard):
            lines = self.ax.get_lines()
            #print("removing...")
            lines[-1].remove()
        
        if xmin:
            self.ax.set_xlim(xmin=xmin,xmax=xmax)
        
        self.used_lines = 0
        lines = self.ax.get_lines()
        self.total_lines = len(lines)
        
        #print("Length lol %d" % len(lines))
        self.canvas.draw()
        
        