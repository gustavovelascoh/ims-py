'''
Created on May 13, 2018

@author: gustavo
'''
import tkinter as tk


class ControlBar(tk.Frame):
    
    _next = None
    _start = None
    _stop = None
    
    def __init__(self, master, next_cb=None, start_cb=None, stop_cb=None):
        
        if next_cb:
            self._next = next_cb
        
        if start_cb:
            self._start = start_cb
        
        if stop_cb:
            self._stop = stop_cb    
        
        tk.Frame.__init__(self, master)
        self.master = master    
        toolbar_frame = tk.Frame(master)
        nbutton = tk.Button(toolbar_frame, text="Next",
                           command=self._next)
        nbutton.pack(side="left")
        lbutton = tk.Button(toolbar_frame, text="Start",
                           command=self._start)
        lbutton.pack(side="left")
        sbutton = tk.Button(toolbar_frame, text="Stop",
                           command=self._stop)
        sbutton.pack(side="left")
        toolbar_frame.pack(side="top")
    
    def _null_cb(self):
        pass

if __name__ == "__main__":
    main = tk.Tk()
    main.wm_title("Control Bar")
    # Code to add widgets will go here...
    ControlBar(main).pack()#(side="top", fill="both", expand="True")
    
    tk.mainloop()