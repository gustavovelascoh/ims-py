'''
Created on May 16, 2017

@author: gustavo
'''
from .blob import BoundingBox

class Leg(object):
    '''
    Class for intersection legs
    '''


    def __init__(self, id, type, heading, bbox, lanes):
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
        
    def add_item(self, item):
        self.occupied_area += item.bbox.area
        self.state = self.occupied_area/self.bbox.area
#         print("leg area: %s, bbox area: %s, occupied area: %s" %
#               (self.bbox.area,item.bbox.area,self.occupied_area))
#         print("Leg bbox %s, item bbox: %s" % (self.bbox, item.bbox))
    
    def is_in(self, item):
        
        return self.bbox.is_in(item.bbox.center)
    
    def check_item(self, item):
        
        if self.is_in(item):
            self.add_item(item)
    
    def clear(self):
        self.occupied_area = 0