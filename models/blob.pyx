'''
Created on May 7, 2017

@author: gustavo
'''
import numpy as np
from math import ceil


class Blob(object):
    '''
    classdocs
    '''

    def __init__(self, data, ts, nf, blob_id):
        self.data = data
        self.ts = ts
        self.nf = nf
        self.id = blob_id
        self.next_blobs = []
        self.prev_blobs = []
        self.vel = None
        self.ang = None
        
    def get_features(self):
        xy = self.data
        bbox = np.array([min(xy[:,0:1]), min(xy[:,1:2]),max(xy[:,0:1]), max(xy[:,1:2])])
        self.bbox = BoundingBox((bbox[0], bbox[1]), (bbox[2], bbox[3]))        
        self.dens = len(xy)/self.bbox.area
        self.mean = xy.mean(axis=0)
        
    def get_distance_from(self, blob):
        return abs(np.linalg.norm(self.mean - blob.mean))
    
    def set_connection_from(self, blob):
        self.prev_blobs = blob.prev_blobs + [blob.id]
        blob.next_blobs.append(self.id)
        
        self.vel = self.get_distance_from(blob)/(self.ts - blob.ts)
        self.ang = self._angle_between(self.mean, blob.mean)
    
    def add_connection_to(self, blob):
        self.next_blobs.append(blob.id)

    @staticmethod
    def _unit_vector(vector):
        """ Returns the unit vector of the vector.  """
        return vector / np.linalg.norm(vector)

     
    def _angle_between(self, v1, v2):
        v1_u = self._unit_vector(v1)
        v2_u = self._unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    
class BoundingBox(object):
    
    minxy = None
    maxxy = None
    width = None
    height = None
    area = None
    center = None
    
    def __init__(self, minxy, maxxy):
        '''
        @param minxy: Tuple of min coordinate point of bounding box e.g. (0,0)
        @param maxxy: Tuple of max coordinate point of bounding box e.g. (2,5)
        '''
        
        self.minxy = minxy
        self.maxxy = maxxy
        
        dx = maxxy[0] - minxy[0]
        dy = maxxy[1] - minxy[1]
        
        dx_cm = dx * 100
        dy_cm = dy * 100
        
        grid_k = 50
        
        self.width = (ceil((dx_cm) / grid_k)*grid_k)/100
        self.height = (ceil((dy_cm) / grid_k)*grid_k)/100
        self.area = self.width * self.height
        self.center = (minxy[0]+(self.width/2), minxy[1]+(self.height/2))
    
    def is_in(self, point):
        '''
        Tests if a point is inside the bounding box
        @param point: tuple of coordinate point (x,y)
        @return: Boolean, True if point is inside bbox, False otherwise. 
        '''
        
        ret = False
        
        if point[0] >= self.minxy[0] and point[0] <= self.maxxy[0]:
            if point[1] >= self.minxy[1] and point[1] <= self.maxxy[1]:
                ret = True
            
        return ret
    
    def __str__(self, *args, **kwargs):
        blob_str = "minxy: (%s,%s)"  % (self.minxy)
        blob_str += "maxxy: (%s,%s)"  % (self.maxxy)
        return blob_str
    
    