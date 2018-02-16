'''
Created on Dec 25, 2017

@author: gustavo
'''
import numpy as np
from gui.Plotter2D import Plotter2D
from models.subscriber import Subscriber
import tkinter as tk
import json

BUFF_SIZE = 100

time_array = np.array([])
data_array = np.array([])


main = tk.Tk()
main.wm_title("Legs State Plotter")
# Code to add widgets will go here...
p = Plotter2D(main)
p.pack()

def subscriber_cb(msg):
    
    global time_array
    global data_array
    
    print(msg)
    
    payload = json.loads(msg["data"].decode("utf-8"))
    print(payload)
   
    time_array = np.append(time_array, payload["ts"])
    print(time_array)
    
    curr_data_array = np.array([payload["legs_state"]])
    
    print(np.shape(curr_data_array))
    print(curr_data_array)
    print(np.transpose(curr_data_array))
    print(np.shape(data_array))
        
    if np.shape(data_array)[0] == 0:
        data_array = np.transpose(curr_data_array)
    else:
        data_array = np.concatenate((data_array, np.transpose(curr_data_array)), axis=1)
    
    print(data_array)
    
    for dat in data_array:
        p.plot(time_array, dat)
    
    p.update(xmin=time_array[0], xmax=time_array[-1], ymin=0, ymax=1)

s = Subscriber({"ims/legs/state_og": subscriber_cb})
s.run()
tk.mainloop()