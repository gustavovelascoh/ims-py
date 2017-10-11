'''
Created on Oct 3, 2017

@author: gustavo
'''
from models.occupancygrid import OccupancyGrid as og
import numpy as np
from matplotlib import pyplot as plt




if __name__ == '__main__':
    o = og(-30, -24, 40, 30, cell_size=0.1)
    o.set_origin(0,0)
    x_test = np.array([10,10,10,10, 10, 10, 9, 8, 7, 6, 5, 4 ])
    y_test = np.array([10,12, 15,17,18,20,25, 26, 27, 28,29, 30])    
    o.add_meas(x_test, y_test)
    o.update()
    x_test += 1
    o.add_meas(x_test, y_test)
    o.update()
    x_test += 1
    o.add_meas(x_test, y_test)
    o.update()
    x_test += 1 
    o.add_meas(x_test, y_test)
    o.update()
    im = plt.imshow(o.grid, cmap='gray')
    plt.colorbar(im, orientation='horizontal')
    plt.show()