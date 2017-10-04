'''
Created on Oct 2, 2017

@author: gustavo
'''
import numpy as np

class OccupancyGrid(object):
    '''
    classdocs
    '''


    def __init__(self, xmin, ymin, xmax, ymax, cell_size=0.3):
        '''
        Constructor
        '''
        self.xmin = xmin
        self.ymin = ymin
        self.cell_size = cell_size
        
        dx = xmax-xmin
        dy = ymax-ymin
        
        self.cols = np.ceil(dx/cell_size) + 1
        self.rows = np.ceil(dy/cell_size) + 1
        
        self.grid=0.5*np.ones((self.rows, self.cols))
        print((np.shape(self.grid)))
        
    def point2index(self, x, y):
        col = np.ceil((x - self.xmin)/self.cell_size - 0.5)
        row = np.ceil((y - self.ymin)/self.cell_size - 0.5)
        return col, row
    
    def set_origin(self, xo, yo):
        self.xo = xo
        self.yo = yo
        
        self.col_o, self.row_o = self.point2index(xo, yo)
        self.mark_fill(xo, yo)
    
    def mark_fill(self, x, y, val=0.9):
        col, row = self.point2index(x, y)        
        self.grid[row,col] = val
    
    def mark_empty(self,x, y):
        col, row = self.point2index(x, y)
        if (self.grid[row,col]== 0.5):
            self.grid[row,col] = 0.1
    
    def add_point_set(self, xs, ys):
        
        dxs = xs - self.xo
        dys = ys - self.yo

        m = dys/dxs
        print("m: ", m)
        b = ys - m*xs
        
        for x, y, mc, bc in zip(xs, ys, m, b):
            self.mark_fill(x, y)
            
            xt_0 = x if x < self.xo else self.xo
            xt_1 = x if x > self.xo else self.xo

            xt = np.ogrid[xt_0:xt_1:0.5*self.cell_size]
            yt = mc*xt + bc
            
            for xe, ye in zip(xt, yt):
                self.mark_empty(xe, ye)
            
        
        
        
        
        