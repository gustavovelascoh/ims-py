'''
Created on May 16, 2017

@author: gustavo
'''
import tkinter as tk
from tkinter import filedialog

class DatasetConfig(tk.Frame):
    def __init__(self, master,create_cb=None,default_file="scene.imscfg"):
        '''
        Constructor
        '''
        tk.Frame.__init__(self, master)
        self.master = master
        l = tk.Label(self, text="Select dataset config file")
        l.grid(row=0, column=0)
        self.e = tk.Entry(self)
        self.e.grid(row=0, column=1)
        self.e.insert(0,default_file)
        button_b = tk.Button(self, text="Browse", command=self.select_file, 
                           width=10)
        button_b.grid(row=0, column=2)
        button_c = tk.Button(self, text="Create Scene",
                           command=create_cb)
        button_c.grid(row=0, column=3)
        
        self.rec_check = 0
        self.rec_check_tk = tk.IntVar()
        rec_ch_btn = tk.Checkbutton(self,
                                     text="Save data to file",
                                     variable=self.rec_check_tk,
                                     command=self.__rec_check_cb)
        
        rec_ch_btn.grid(row=0, column=4)
        
        self.filename = default_file
    
    def __rec_check_cb(self):
        self.rec_check = self.rec_check_tk.get()
    
    def select_file(self):
        ims_path="/home/gustavo/devel/python/ims/possi"
        self.dataset_path = ims_path
        print("hello button")
        print(hasattr(tk,"filedialog"))        
        self.filename = tk.filedialog.askopenfilename(
            initialdir=ims_path,
            filetypes=[('IMS config file','*.imscfg')])
        if self.filename:
            print("FOLDER OK -> %s" % self.filename)
        self.e.insert(0, self.filename)
    
    
class RangeSensors(tk.Frame):
    def __init__(self, master):
        '''
        Constructor
        '''
        tk.Frame.__init__(self, master)
        self.master = master
        l = tk.Label(self, text="Range Sensors",font=("Helvetica", 16))
        l.grid(row=0, columnspan=2)
        
        tk.Label(self, text="Name",font=("Helvetica", 14)).grid(row=1, column=0)
        tk.Label(self, text="Type",font=("Helvetica", 14)).grid(row=1, column=1)
        self.curr_row = 2
    
    def add_rows(self, sensors):
        
        for s in sensors:
            tk.Label(self, text=s["name"],font=("Helvetica", 12)).grid(row=self.curr_row, column=0)
            tk.Label(self, text=s["subtype"],font=("Helvetica", 12)).grid(row=self.curr_row, column=1)            
            self.curr_row += 1
        
        
class Cameras(tk.Frame):
    def __init__(self, master):
        '''
        Constructor
        '''
        tk.Frame.__init__(self, master)
        self.master = master
        l = tk.Label(self, text="Cameras",font=("Helvetica", 16))
        l.grid(row=0, columnspan=2)
        
        tk.Label(self, text="Name",font=("Helvetica", 14)).grid(row=1, column=0)
        tk.Label(self, text="Type",font=("Helvetica", 14)).grid(row=1, column=1)
        self.curr_row = 2
        
    def add_rows(self, cameras):
        if cameras == {} or cameras is None:
            msg = "No cameras available"
            tk.Label(self, text=msg, font=("Helvetica", 14), pady=25).grid(row=self.curr_row, columnspan=2)

class LegsState(tk.Frame):
    '''
    Legs state viewer
    '''
    def __init__(self, master):
        '''
        Constructor
        '''
        tk.Frame.__init__(self, master)
        self.config(bd=3)
        self.master = master
        tk.Label(self, text="Legs State",font=("Helvetica", 16)).grid(row=0, columnspan=3)
        
        tk.Label(self, text="Leg ID",font=("Helvetica", 14),width=8).grid(row=1, column=0)
        tk.Label(self, text="Status",font=("Helvetica", 14),width=30).grid(row=1, column=1)
        
        self.status_labels = []
        
        self.curr_row = 2
    
    def add_rows(self, legs):
        
        for leg in legs:
            tk.Label(self, text=leg["id"],font=("Helvetica", 12)).grid(row=self.curr_row, column=0)
            st_l = tk.Label(self, text="*****")
            st_l.grid(row=self.curr_row, column=1)
            self.status_labels.append(st_l)            
            self.curr_row += 1

        
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
        tk.Label(self, text="Legs Info",font=("Helvetica", 16)).grid(row=0, columnspan=3)
        
        tk.Label(self, text="ID",font=("Helvetica", 14)).grid(row=1, column=0)
        tk.Label(self, text="Type",font=("Helvetica", 14)).grid(row=1, column=1)
        tk.Label(self, text="Heading",font=("Helvetica", 14)).grid(row=1, column=2)
        
        self.curr_row = 2
    
    def add_rows(self, legs):
        
        for leg in legs:
            tk.Label(self, text=leg["id"],font=("Helvetica", 12)).grid(row=self.curr_row, column=0)
            tk.Label(self, text=leg["type"],font=("Helvetica", 12)).grid(row=self.curr_row, column=1)
            tk.Label(self, text=leg["heading"],font=("Helvetica", 12)).grid(row=self.curr_row, column=2)
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