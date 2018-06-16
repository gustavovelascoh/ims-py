'''
Created on Jun 16, 2018

@author: gustavo
'''
import json
import time
import numpy as np


class Points2OccGrid():
    def __init__(self, in_ch="", out_ch=""):
        pass

if __name__ == "__main__":
    
    import argparse
    
    description_str='Subscribe to cartesian data and generate occgrid'
    parser = argparse.ArgumentParser(description=description_str)
    parser.add_argument('ich',
                        metavar='ICH',
                        help="Input channel")
    parser.add_argument('och',
                        metavar='OCH',
                        help="Output channel")
    args = parser.parse_args()
    
    p2c = Points2OccGrid(in_ch=args.ich, out_ch=args.och)
