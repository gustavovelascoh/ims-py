'''
Created on Nov 23, 2017

@author: gustavo
'''
import pickle
import numpy as np

from matplotlib import pyplot as plt


filename = "../possi_123578.cs03th06a.data"
data = None
with open(filename,"rb") as f:
    data = pickle.load(f)
    
print(np.shape(data))
print(data[0])

ts = np.array([])
legs_state = np.array([])

for f in data:
    ts = np.append(ts, f["ts"])
    legs_array = np.array([f["legs_state"]])
    if len(legs_state) == 0:
        legs_state = legs_array.T
    else:
        legs_state = np.concatenate((legs_state,legs_array.T), axis=1)
print(np.shape(ts))
print(np.shape(legs_state))

# plt.subplot(2,2,4)
plt.plot(legs_state.T)

plt.show()
    
    