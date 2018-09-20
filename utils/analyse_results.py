import numpy as np

GT_FILE = "gt_results.csv"
VID_FILE = "video_results_75_cbt.csv"
LAS_FILE = "laser_results.csv"


def load_results_file(filename):
    results = []
    v=True      
    with open(filename,'rb') as f:
            
        while v:
            v = f.readline()
            if v == b'':
                break
            results.append(round(float(v[:-1])))

    return results

def group_data(data, group):
    curr_len = len(data)
    new_len = int(np.floor(curr_len/group))
    end_idx = group*new_len-curr_len

    if end_idx != 0:
        data_g = np.reshape(data[0:end_idx],
			     (group,new_len))
    else:
        data_g = np.reshape(data[0:],
			     (group,new_len))
    return data_g

def count_cars(gt):
    
    gt_c = [0]
    
    # count cars, transitions
    for i in range(1,len(gt)):
        
        d = gt[i] - gt[i-1]
#        print(d)
        if d < -0.33:
            gt_c.append(1)
        else:
            gt_c.append(0)

    return gt_c

def get_flow_bin(count_data, group=30):
    
    cnt_g = group_data(count_data, group)

    flow = np.sum(cnt_g,axis=0)/(group/30)

    flow_bin = flow > 0.5

    return flow_bin


def max_window(r):
    l = len(r)
    lw = np.copy(r)
    
#    print(l, r[0:15])
    for i in range(1,l-1):
#        print(r[i-1:i+2])
        lw[i] = np.max(r[i-1:i+2])

    return lw

def avg_round(r):
    l = len(r)
    lw = np.copy(r)
    
#    print(l, r[0:15])
    for i in range(3,l-3):
#        print(r[i-1:i+2])
        lw[i] = np.round(np.mean(r[i-3:i+4]))

    return lw

def compare_detections(gt, res):
    raw_error = gt - res
    print(gt, res)
#    exit()
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for i, v in enumerate(gt):

        if raw_error[i] == 0 and v != 0:
            TP += v
        elif raw_error[i] == 0 and v == 0:
            TN += 1
        elif raw_error[i] > 0:
            FN += raw_error[i]
            #TP += v-raw_error[i]
        elif raw_error[i] < 0:
            FP -= raw_error[i]
            #TP -= v + raw_error[i]

#    print("TP: {0}, FN: {1}".format(TP,FN))
#    print("FP: {0}, TN: {1}".format(FP,TN))
    print( {"TP": TP,"FP": FP, "TN": TN, "FN": FN})
    return {"TP": TP,"FP": FP, "TN": TN, "FN": FN}

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
        
#    print("TP: {0}, FN: {1}".format(TP,FN))
#    print("FP: {0}, TN: {1}".format(FP,TN))
    print({"TP": TP,"FP": FP, "TN": TN, "FN": FN})
    return {"TP": TP,"FP": FP, "TN": TN, "FN": FN}

# cm is a dict {"TP": TP,"FP": FP, "TN": TN, "FN": FN}
def get_metrics(cm):
    tptn = cm["TP"]+cm["TN"]
    fpfn = cm["FP"]+cm["FN"]
    tpfn = cm["TP"]+cm["FN"]
    fptn = cm["FP"]+cm["TN"]

    metrics = {}
    metrics["accu"] = tptn/(tptn+fpfn)
    metrics["prec"] = cm["TP"]/(cm["TP"]+cm["FP"])
    metrics["reca"] = cm["TP"]/tpfn
    metrics["spec"] = cm["TN"]/fptn
    metrics["F1"] = 2*cm["TP"]/(2*cm["TP"]+fpfn)
    metrics["prev"] = tpfn/(tpfn+fptn)
    
    metrics["TPR"] = metrics["reca"]
    metrics["FPR"] = 1 - metrics["spec"]

    metrics["PPV"] = (metrics["reca"]*metrics["prev"])/(metrics["reca"]*metrics["prev"]+metrics["FPR"]*(1-metrics["prev"]))
    metrics["NPV"] = (metrics["reca"]*(1-metrics["prev"]))/((1-metrics["reca"])*metrics["prev"]+metrics["spec"]*(1-metrics["prev"]))

    return metrics

def evaluate_results(offset=45, grouping=0):
    pass


if __name__ == "__main__":

    gt = []
    vid = []
    las = []
    gt = load_results_file(GT_FILE)
    vid  = load_results_file(VID_FILE)
    las = load_results_file(LAS_FILE)
    gt = np.array(gt)
    vid = np.array(vid)
    las = np.array(las)

    vid = avg_round(vid)
#    las = avg_round(las)
#    vid = las
#    vid = np.round((vid + las) /2)



    #print(len(gt), len(vid))
    #print("shape gt: {0}, shape vid: {1}".format(
    #                                            np.shape(gt),
    #                                            np.shape(vid)
    #
    #                                            ))

    scores = []
    best_score = 0

    for j in range(1,2):

        for i in range(-80,80):
            
            if i < 0:
                gt_temp = gt[0:i]
                vid_temp = vid[-i:]
            elif i > 0:
                gt_temp = gt[i:]
                vid_temp = vid[0:-i]
            else:
                gt_temp = gt
                vid_temp = vid

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
            
    #        print(len(gt_c), j*new_len,new_len)
            
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
                
            gt_c_rs = np.sum(gt_c_rs,axis=0)
            vid_c_rs = np.sum(vid_c_rs,axis=0)
             
            print("Count GTrs: ", sum(gt_c_rs)) 
            print("Count vidrs: ", sum(vid_c_rs)) 
            
            gt_fb = get_flow_bin(gt_c_rs,30)
            vid_fb = get_flow_bin(vid_c_rs,30)

    #        print("NEW SHAPE ", np.shape(vid_c_rs))
            
    #        print(vid_c_rs)
            
#            score = compare_gt (vid_c_rs,gt_c_rs)
#            score = compare_detections (gt=gt_temp, res=vid_temp)
            score = compare_detections (gt=gt_fb, res=vid_fb)
            metrics = get_metrics(score)
            curr_score = metrics["TPR"] 
            
            if best_score < curr_score:
                best_score = curr_score
                print("BEST NEW= ", metrics, score, i, j)
            
            scores.append(curr_score)
        
        

    print("Best score", np.max(score))
    exit()


