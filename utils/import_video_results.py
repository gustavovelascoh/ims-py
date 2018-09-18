import re

RE_STR = "[0-9]+"
b = re.compile(RE_STR)


def get_percentage(perc_str):
    pc_str = b.search(perc_str).group()
    return int(pc_str)

def find_overlap(pts_a, pts_b):
    a = pts_a[0]
    b = pts_a[1]
    c = pts_a[2]
    d = pts_a[3]    
    e = pts_b[0]
    f = pts_b[1]
    g = pts_b[2]
    h = pts_b[3]
    
    overlap = [max([a,e]), max([b,f]),
               min([c,g]), min([d,h])]
    #print("overlap",overlap)
    if overlap[0] > overlap[2] or overlap[1] > overlap[3]:
        overlap = None
        
    return overlap
        
FILENAME="/home/gustavo/devel/personal/python/ims-py/video_possi.results"

frame_n = 1
results = []
with open(FILENAME,'r') as f:

    #try:
    for line in f:    
        #line = f.readline()
    
        line_list = line.split(" ")
        
        objects = []
        
        line_len = len(line_list)
        curr_offset = 0
        
        if line_len == 0:
            f.close()
        
        # > len 3 because after split '\n' is the last element
        if line_len > 3:
            curr_offset = 2
            #print(line_list)
            while curr_offset + 8 < line_len:
            
                if line_list[curr_offset+2] == 'Bounding':
                    curr_obj_list = line_list[curr_offset:curr_offset+8]
                else:
                    curr_obj_list = line_list[curr_offset:curr_offset+10]
                    
                if curr_obj_list[0] == 'car:' and get_percentage(curr_obj_list[1])>90:
                    
                    curr_obj_os = 0 if len(curr_obj_list) == 8 else 2
                    
                    #print(curr_obj_list)
                    bbox = []
                    # bbox saved as [left, top, right, bottom]
                    bbox.append(int(curr_obj_list[curr_obj_os+4].split('=')[1][:-1]))
                    bbox.append(int(curr_obj_list[curr_obj_os+5].split('=')[1][:-1]))
                    bbox.append(int(curr_obj_list[curr_obj_os+6].split('=')[1][:-1]))
                    bbox.append(int(curr_obj_list[curr_obj_os+7].split('=')[1][:]))
                    
                    #check in vsens (612,473) (1133,656)
                    vsens1 = [930, 550, 1118, 603]
                    vsens2 = [652, 601, 994, 661]
                    vsens3 = [700, 661, 950, 720]
                    vsens4 = [1030, 500, 1118, 550]
                    #print(bbox)
                    
                    if (find_overlap(vsens1, bbox) or 
                        find_overlap(vsens2, bbox) or 
                        find_overlap(vsens3, bbox) or 
                        find_overlap(vsens4, bbox)):
                        objects.append(bbox)
                    #print("objects: {0}".format(objects))
                
                curr_offset += 8
            
            
        else:
            pass
                    
        results.append(objects)
        print("{0},{1}".format(frame_n, len(objects)))
        frame_n += 1
#     except Exception as e:
#         print(e)        
#         f.close()
        #continue
for i, l in enumerate(results): 
    #print("*",i,l)
    pass
#print(len(results))
    