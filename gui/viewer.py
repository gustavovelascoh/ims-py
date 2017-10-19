'''
Created on Jan 16, 2017

@author: gustavo
'''
import tkinter as tk
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches


class Viewer(tk.Frame):
    '''
    classdocs
    '''    
    def __init__(self, master, figsize=None):
        '''
        Constructor
        '''        
        tk.Frame.__init__(self, master)
        
        self.master = master
        self.roi = None
        self.loop = False
        if figsize == None:
            figsize = (30/3,22.5/3)
        self.fig = Figure(figsize=figsize)
        #ax = fig.add_subplot(111, projection='polar')
        self.ax = self.fig.add_subplot(111)
         
        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.fixed_lines = 0
        self.total_lines = 0
        self.used_lines = 0
        self.bg_saved = 0
        
        self.boxes = {"fixed": 0,
                       "total": 0,
                       "used": 0}
        
        self.boxes_list = []
        self.array = None
        
    def draw_img(self, img_path, limits=None):
        img = mpimg.imread(img_path)
        imgplot = self.ax.imshow(img, aspect='auto', extent=limits)
        self.__fit_to_roi()
        self.canvas.show()
    
    def draw_array(self, array, limits=None):
        if self.array is None:
            self.array = self.ax.imshow(array, aspect='auto', extent=limits, cmap='gray')
            self.__fit_to_roi()
            self.canvas.show()
        else:
            self.array.set_data(array)
            self.__fit_to_roi()
            self.canvas.show()
        
    def __fit_to_roi(self):
        if self.roi != None:
            self.ax.set_ylim(ymin=self.roi["ymin"],ymax=self.roi["ymax"])
            self.ax.set_xlim(xmin=self.roi["xmin"],xmax=self.roi["xmax"])    
        
     
    def set_roi(self, roi): 
        self.roi = roi
     
    def plot(self, *args, **kwargs):
        
        self.available_lines = self.total_lines - self.fixed_lines - self.used_lines
#         print("Available lines: %d-%d-%d : %d" % (self.total_lines,
#                                                self.fixed_lines,
#                                                self.used_lines,
#                                                self.available_lines))
        if self.available_lines > 0:
#             print("Updating line ")
            line_idx = (self.fixed_lines + self.used_lines)            
            self.__update_plot_data( *args, line_idx=line_idx)
            self.update_style(line_idx, **kwargs)
            
        else:
#             print("Creating new line")
            self.ax.plot(*args, **kwargs)
            self.update_style(line_idx="last", **kwargs)
            self.__fit_to_roi()
            #self.canvas.show()
            self.total_lines = len(self.ax.get_lines())
        
        if self.bg_saved:    
            self.used_lines += 1
        
            
    def save_background(self):
        self.__fit_to_roi()
        self.canvas.show()
        self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)
#         self.plot_data_tup = self.ax.plot(0, 0, 'b. ')
#         print("tuple")
#         print(self.plot_data_tup)
#         self.cur_lines = len(self.plot_data_tup)
#         self.plot_data = self.plot_data_tup[0]
        self.canvas.show()
        self.fixed_lines = len(self.ax.get_lines())
        self.boxes["fixed"] = len(self.ax.patches)
        
        self.bg_saved = 1
    
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
        #self.canvas.draw()
        #return self.plot_data
    
    def update_style(self, line_idx, **kwargs):
        list_of_lines = self.ax.get_lines()
        if line_idx == "last":
            curr_line = list_of_lines[-1]
        else:
            curr_line = list_of_lines[line_idx]
        
        if "color" in kwargs.keys():        
            curr_line.set_color(kwargs["color"])
        else:
            curr_line.set_color("blue")
        
        if "marker" in kwargs.keys():        
            curr_line.set_marker(kwargs["marker"])
        else:
            curr_line.set_marker(" ")
        
        if "linestyle" in kwargs.keys():        
            curr_line.set_linestyle(kwargs["linestyle"])
        else:
            curr_line.set_linestyle('-')
        
        self.ax.draw_artist(curr_line)
    
    def add_plot(self, *args, **kwargs):
        self.ax.plot(*args, **kwargs)
        self.__fit_to_roi()
        #self.canvas.show()
        self.total_lines = len(self.ax.get_lines())
    
    def update(self):
        
        
        lines_to_discard = self.total_lines - self.fixed_lines - self.used_lines
        #print("l2d: %d", lines_to_discard)
        
        lines = self.ax.get_lines()
        #print("Length lol %d" % len(lines))
        for i in range(0,lines_to_discard):
            lines = self.ax.get_lines()
            #print("removing...")
            lines[-1].remove()
        
        boxes_to_discard = self.boxes["total"] - self.boxes["fixed"] - self.boxes["used"]
        
        for i in range(0,boxes_to_discard):
            self.boxes_list[-1].remove()
            del self.boxes_list[-1]
        
        self.used_lines = 0
        lines = self.ax.get_lines()
        self.total_lines = len(lines)
        self.boxes["used"] = 0
        self.boxes["total"] = len(self.boxes_list)
        #print("Length lol %d" % len(lines))
        self.canvas.draw()
    
    def plot_box(self,minx, miny, dx, dy,fill=False, edgecolor="green"):
        
        self.boxes["total"] = len(self.boxes_list)
        available_boxes = self.boxes["total"] - self.boxes["fixed"] - self.boxes["used"]
#         print("Available boxes: %d-%d-%d : %d" % (self.boxes["total"],
#                                                self.boxes["fixed"],
#                                                self.boxes["used"],
#                                                available_boxes))
        if available_boxes > 0:
            
            av_idx = self.boxes["fixed"]
            av_idx += self.boxes["used"]
            
            curr_box = self.boxes_list[av_idx]
            
            curr_box.set_bounds(minx, miny, dx, dy)
            curr_box.set_fill(fill)
            curr_box.set_edgecolor(edgecolor)
            
            
        else:        
            patch = self.ax.add_patch(
             patches.Rectangle(
                (minx, miny),
                dx,
                dy,
                fill=fill,      # remove background
                edgecolor=edgecolor
             ) )
            
            self.boxes_list.append(patch)
            self.boxes["total"] = len(self.boxes_list)
        
        #if (self.bg_saved):
        self.boxes["used"] += 1
        

if __name__ == "__main__":
    main = tk.Tk()
    main.wm_title("IMS Viewer")
    # Code to add widgets will go here...
    Viewer(main).pack()#(side="top", fill="both", expand="True")
    
    tk.mainloop()
        