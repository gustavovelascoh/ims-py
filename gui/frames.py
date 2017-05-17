'''
Created on May 16, 2017

@author: gustavo
'''
import tkinter as tk

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