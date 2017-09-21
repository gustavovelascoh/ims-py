'''
Created on May 16, 2017

@author: gustavo
'''
import numpy as np
from .blob import BoundingBox

class Leg(object):
    '''
    Class for intersection legs
    '''
    

    def __init__(self, id, type, heading, bbox, lanes, buffer_size=90):
        '''
        Constructor
        '''
        self.id = id
        self.type = type
        self.heading = heading
        self.bbox = BoundingBox((bbox[0],bbox[1]),(bbox[2],bbox[3]))
        self.lanes = lanes
        self.state = 0
        self.occupied_area = 0
        self.state_buffer = []
        self.buffer_size = buffer_size
        self.b_idx = 0;
        
    def add_item(self, item):
        self.occupied_area += item.bbox.area
        self.state = self.occupied_area/self.bbox.area
#         print("leg area: %s, bbox area: %s, occupied area: %s" %
#               (self.bbox.area,item.bbox.area,self.occupied_area))
#         print("Leg bbox %s, item bbox: %s" % (self.bbox, item.bbox))
        if self.b_idx < self.buffer_size:
            if len(self.state_buffer) > self.b_idx:
                self.state_buffer[self.b_idx] = self.state
            else:
                self.state_buffer.append(self.state)
        else:
            try:
                if len(self.state_buffer) > self.buffer_size:
                    self.state_buffer[-1] = self.state
                else:
                    self.state_buffer.append(self.state)
                # del self.state_buffer[0]
            except Exception as e:
                print(e)

    def get_state(self):
        if len(self.state_buffer) > self.buffer_size:
            del self.state_buffer[0]
        mean_state = np.mean(self.state_buffer) 
        return mean_state
            
    def is_in(self, item):
        
        return self.bbox.is_in(item.bbox.center)
    
    def check_item(self, item):
        
        if self.is_in(item):
            self.add_item(item)
    
    def clear(self):
        self.occupied_area = 0
        
        if self.b_idx < self.buffer_size:            
            self.b_idx += 1
            if len(self.state_buffer) < self.b_idx:
                self.state_buffer.append(0)
        