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