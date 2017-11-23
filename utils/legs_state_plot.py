'''
Created on Nov 23, 2017

@author: gustavo
'''
import pickle
import numpy as np

filename = "../possi_123578.imscfg.data"

with open(filename,"rb") as f:
    data = pickle.load(f)
    
print(np.shape(data))