import numpy as np

GT_FILE = "gt_results.csv"
VID_FILE = "video_results_90.csv"

def count_cars(gt):
    
    gt_c = [0]
    
    # count cars, transitions
    for i in range(1,len(gt)):
        
        d = gt[i] - gt[i-1]
        
        if d < -0.333:
            gt_c.append(1)
        else:
            gt_c.append(0)

    return gt_c
#import gt

def compare_gt (vid,gt):
    raw_error = gt - vid

    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for i, v in enumerate(gt):

        if raw_error[i] == 0 and v == 1:
            TP += 1
        elif raw_error[i] == 0 and v == 0:
            TN += 1
        elif raw_error[i] > 0:
            FN += 1#raw_error[i]
            #TP += v-raw_error[i]
        elif raw_error[i] < 0:
            FP += 1#raw_error[i]
            #TP -= v + raw_error[i]
        
    print("TP: {0}, TN: {1}".format(TP,TN))
    print("FP: {0}, FN: {1}".format(FP,FN))
    return [TP, FP, TN, FN]

gt = []
vid = []

l = "x"
with open(GT_FILE, 'r') as f:
    while l != "":
        l = f.readline()
        if l == '':
            break
        gt.append(round(float(l)))
    
l = "x"
with open(VID_FILE, 'r') as f:
    while l != "":
        l = f.readline()
        if l == '':
            break
        l = l.split(',')
        
        vid.append(float(l[1]))
    


gt = np.array(gt)
vid = np.array(vid)
print(len(gt), len(vid))
print("shape gt: {0}, shape vid: {1}".format(
                                            np.shape(gt),
                                            np.shape(vid)
                                            ))
scores = []
best_score = 0

for j in range(3,15):

    for i in range(1,300):
        
        gt_temp = gt[0:-i]
        vid_temp = vid[i:]
    
        gt_c = [0]
        vid_c = [0]
        # count cars, transitions
        gt_c = count_cars(gt_temp)
        vid_c = count_cars(vid_temp)
        
        
            
        print("Count GT: ", sum(gt_c)) 
        print("Count vid: ", sum(vid_c))    
        
        curr_len = len(gt_c)
        new_len = int(np.floor(curr_len/j))
        end_idx = j*new_len-curr_len
        
        print(len(gt_c), j*new_len,new_len)
        
        if end_idx != 0:
        
            gt_c_rs = np.reshape(gt_c[0:end_idx],
                                 (j,new_len))
            vid_c_rs = np.reshape(vid_c[0:end_idx],
                                 (j,new_len))
        else:
            gt_c_rs = np.reshape(gt_c[0:],
                                 (j,new_len))
            vid_c_rs = np.reshape(vid_c[0:],
                                 (j,new_len))
            
        gt_c_rs = np.max(gt_c_rs,axis=0)
        vid_c_rs = np.max(vid_c_rs,axis=0)
         
        print("Count GTrs: ", sum(gt_c_rs)) 
        print("Count vidrs: ", sum(vid_c_rs)) 
        
        print("NEW SHAPE ", np.shape(vid_c_rs))
        
        print(vid_c_rs)
        
        score = compare_gt (vid_c_rs,gt_c_rs)
        
        curr_score = score[0]/(score[0]+score[3])
        
        if best_score < curr_score:
            best_score = curr_score
            print("BEST NEW= ", score, curr_score, i, j)
        
        scores.append(curr_score)
    
    

print("Best score", np.max(score))
exit()

    
