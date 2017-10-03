'''
Created on Oct 2, 2017

@author: gustavo
'''
import numpy as np

class OccupancyGrid(object):
    '''
    classdocs
    '''


    def __init__(self, xmin, ymin, xmax, ymax, grid_size=0.3):
        '''
        Constructor
        '''
        dx = xmax-xmin
        dy = ymax-ymin
        
        self.cols = np.ceil(dx/grid_size)
        self.rows = np.ceil(dy/grid_size)
        
        self.grid=0.5*np.ones((self.rows, self.cols))
        print((np.shape(self.grid)))
        