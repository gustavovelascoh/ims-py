import argparse
import pickle
import os
import struct
from _operator import mod

def pdk(a,level=0):
    t=''.join(['.' for x in range(0,level)])
    if isinstance(a,dict):
        for k in a.keys():
            print("%s %s:"%(t,k))
            pdk(a[k],level+1)

cwd = os.getcwd()

parser = argparse.ArgumentParser(description='Import possi laser dataset')
parser.add_argument('file', metavar='file',
                    help='dataset file')
parser.add_argument('output_file', metavar='output_file',
                    help='pickle file')
parser.add_argument('name', metavar='name',
                    help='variable name')

args = parser.parse_args()
print("File: %s" % args.file)
print("outputfile: %s" % args.output_file)
print("variable name: %s" % args.name)

f = open(args.file, "rb")
fo = open(args.output_file, "wb")

data={}


try:
    bytes_data = f.read(4)    
    ang_range = struct.unpack('f', bytes_data)[0]
    data["ang_range"] = ang_range
    
    bytes_data = f.read(4)
    ang_res = struct.unpack('f', bytes_data)[0]
    data["ang_res"] = ang_res
    
    bytes_data = f.read(4)
    range_unit = struct.unpack('f', bytes_data)[0]
    data["range_unit"] = range_unit
    
    print(data)
    
    maxlen = ang_range/ang_res + 1
    
    print("maxlen: %s" % maxlen)
    
    data["scans"] = []
    
    scan_n = 0
    
    while True:
    
        scan={"ms":0, 'data':[]}
        
        bytes_data = f.read(4)
        
        if not bytes_data:
            print("**END** scan # %d" % scan_n)
            break
        
        scan['ms'] = int.from_bytes(bytes_data, 'little', signed=False)    
            
        for i in range(0, int(maxlen)):
            bytes_data = f.read(2)
            
            meas = int.from_bytes(bytes_data, 'little', signed=False)
            scan['data'].append(meas)
        
        
        if mod(scan_n,100) == 0:
            print("scan # %d" % scan_n)    
            print(scan)
        
        scan_n+=1
        data["scans"].append(scan)
    #bytes_data = f.read(4+2*maxlen)
    
finally:
    f.close()
    print(len(data["scans"]))
    
    

data["bg_model"] = {}

temp = args.file[0:-4]
print("temp %s" % temp)
bg_file = temp + "bg" + args.file[-1]
calib_file = temp + "calib"

print("bgfile: %s" % bg_file)

f = open(bg_file, "rb")

try:
    bytes_data = f.read(4)
        
    if not bytes_data:
        print("**END** scan # %d" % scan_n)
    
    else:
        scan['ms'] = int.from_bytes(bytes_data, 'little', signed=False)    
        
        for i in range(0, int(maxlen)):
            bytes_data = f.read(2)
        
            meas = int.from_bytes(bytes_data, 'little', signed=False)
            scan['data'].append(meas)
finally:
    print("bg_model %s" % scan)
    data["bg_model"]=scan
    f.close()
    #pickle.dump(data, fo, pickle.HIGHEST_PROTOCOL)
    
data["calib_data"] = {}


with open(calib_file) as cf:
    while True:
        line = cf.readline()
        if line:
            print(line)
            print(line[0:4])
            
            if line[0:4] == "LD "+args.file[-1]:
                line_data = line.split(" ")
                data["calib_data"]["ang"] = line_data[2]
                data["calib_data"]["sx"] = line_data[3]
                data["calib_data"]["sy"] = line_data[4]
                break

pickle.dump(data, fo, pickle.HIGHEST_PROTOCOL)

pdk(data)