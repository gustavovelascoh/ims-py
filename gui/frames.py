'''
Created on May 16, 2017

@author: gustavo
'''
import tkinter as tk

class DatasetConfig(tk.Frame):
    def __init__(self, master,create_cb=None):
        '''
        Constructor
        '''
        tk.Frame.__init__(self, master)
        self.master = master
        l = tk.Label(self, text="Select dataset config file")
        l.grid(row=0, column=0)
        self.e = tk.Entry(self)
        self.e.grid(row=0, column=1)
        button_b = tk.Button(self, text="Browse", command=self.select_file, 
                           width=10)
        button_b.grid(row=0, column=2)
        button_c = tk.Button(self, text="Create Scene",
                           command=create_cb)
        button_c.grid(row=0, column=3)
    
    def select_file(self):
        pass
    
    
class RangeSensors(tk.Frame):
    def __init__(self, master):
        '''
        Constructor
        '''
        tk.Frame.__init__(self, master)
        self.master = master
        l = tk.Label(self, text="Range Sensors")
        l.grid(row=0, columnspan=2)
        
        tk.Label(self, text="Name").grid(row=1, column=0)
        tk.Label(self, text="Type").grid(row=1, column=1)
        self.curr_row = 2
    
    def add_rows(self, sensors):
        
        for s in sensors:
            tk.Label(self, text=s["name"]).grid(row=self.curr_row, column=0)
            tk.Label(self, text=s["subtype"]).grid(row=self.curr_row, column=1)            
            self.curr_row += 1
        
        
class Cameras(tk.Frame):
    def __init__(self, master):
        '''
        Constructor
        '''
        tk.Frame.__init__(self, master)
        self.master = master
        l = tk.Label(self, text="Cameras")
        l.grid(row=0, columnspan=2)
        
        tk.Label(self, text="Name").grid(row=1, column=0)
        tk.Label(self, text="Type").grid(row=1, column=1)
        self.curr_row = 2
        
    def add_rows(self, cameras):
        if cameras is {}:
            msg = "No cameras available"
            tk.Label(self, text=msg).grid(row=self.curr_row, columnspan=2)
        
class Legs(tk.Frame):
    '''
    Legs info viewer
    '''


    def __init__(self, master):
        '''
        Constructor
        '''
        tk.Frame.__init__(self, master)
        self.config(bd=1)
        self.master = master
        tk.Label(self, text="Legs Info").grid(row=0, columnspan=3)
        
        tk.Label(self, text="ID").grid(row=1, column=0)
        tk.Label(self, text="Type").grid(row=1, column=1)
        tk.Label(self, text="Heading").grid(row=1, column=2)
        
        self.curr_row = 2
    
    def add_rows(self, legs):
        
        for leg in legs:
            tk.Label(self, text=leg["id"]).grid(row=self.curr_row, column=0)
            tk.Label(self, text=leg["type"]).grid(row=self.curr_row, column=1)
            tk.Label(self, text=leg["heading"]).grid(row=self.curr_row, column=2)
            self.curr_row += 1
        

if __name__ == "__main__":
    main = tk.Tk()
    main.wm_title("Legs Viewer")
    # Code to add widgets will go here...
    legs_frame = Legs(main)#(side="top", fill="both", expand="True")
    legs_frame.pack()
    
    legs_list = [
        {
        "id": 0,
        "type": "approach",
        "heading": "N",
        "bbox": [0.9, 21.0, 12.5, 30.5],
        "lanes": []
        },
        {
        "id": 1,
        "type": "approach",
        "heading": "E",
        "bbox": [23.0, 2.45, 42.3, 14.0],
        "lanes": []
        },
        {
        "id": 2,
        "type": "departure",
        "heading": "W",
        "bbox": [-30.1, 3.35, -12.72, 14.5],
        "lanes": []
        }            
    ]
    
    legs_frame.add_rows(legs_list)
    
    tk.mainloop()    