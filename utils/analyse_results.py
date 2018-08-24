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
    
    flow = get_flow(count_data, group)

    flow_bin = flow > 0.5

    return flow_bin

def get_flow(count_data, group=30, name="def"):
    flow = np.ndarray(len(count_data))
    for i,v in enumerate(count_data):
        if i < group:
            #print(i,v)
            flow[i] = 30*np.sum(count_data[0:i+1])/(i+1)
        else:
            flow[i] = 30*np.sum(count_data[i-group:i+1])/group
#    print("flo",name, flow[4800:4850])
    return flow
            


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

def compare_bool(gt, res):
    raw_error = gt ^ res
#    print(gt, res)
#    exit()
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for i, v in enumerate(gt):

        if raw_error[i] == 0 and v != 0:
            TP += 1
        elif raw_error[i] == 0 and v == 0:
            TN += 1
        elif raw_error[i] != 0 and v != 0:
            FN += 1
            #TP += v-raw_error[i]
        elif raw_error[i] != 0 and v == 0:
            FP += 1
            #TP -= v + raw_error[i]

#    print("TP: {0}, FN: {1}".format(TP,FN))
#    print("FP: {0}, TN: {1}".format(FP,TN))
#    print( {"TP": TP,"FP": FP, "TN": TN, "FN": FN})
    return {"TP": TP,"FP": FP, "TN": TN, "FN": FN}

def compare_detections(gt, res):
    raw_error = gt - res
#    print(gt, res)
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
#    print( {"TP": TP,"FP": FP, "TN": TN, "FN": FN})
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
#    print({"TP": TP,"FP": FP, "TN": TN, "FN": FN})
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

def evaluate_results(res, gt, group=30, name="default"):
    res_c = count_cars(res)
    gt_c = count_cars(gt)

#    print("cnt", res_c[4800:4850])
    gt_fb = get_flow_bin(gt_c, group)
    res_fb = get_flow_bin(res_c, group)

#    print("fbb", res_fb[4800:4850])
#    print("fbg", gt_fb[4800:4850])    

    score = compare_bool(gt=gt_fb, res=res_fb)
    metrics = get_metrics(score)
    
    print(name, m2str(metrics))

def evaluate_results_f(res1, res2, gt, group=30, method="avg", name="default"):

    MN = 4800
    MX = 4850

#    print("r1 ", res1[MN:MX])
#    print("r2 ", res2[MN:MX])

    res1_c = count_cars(res1)
    res2_c = count_cars(res2)
    gt_c = count_cars(gt)

#    print("r1c", res1_c[MN:MX])
#    print("r2c", res2_c[MN:MX])

    gt_f = get_flow(gt_c, group,name="GT")
    res1_f = get_flow(res1_c, group)
    res2_f = get_flow(res2_c, group)

#    print("r1f", res1_f[MN:MX])
#    print("r2f", res2_f[MN:MX])

    if method == "avg":
        res = np.mean(np.stack((res1_f,res2_f)), axis=0)
    elif method == "max":
        res = np.max(np.stack((res1_f,res2_f)), axis=0)
    else:
        return

#    print("res", res[MN:MX])


    res_fb = res > 0.5
    gt_fb = gt_f > 0.5

#    print("rfb", res_fb[4800:4850])
#    print("rfb", gt_f[4800:4850])

    score = compare_bool(gt=gt_fb, res=res_fb)
    metrics = get_metrics(score)

    print(name, m2str(metrics))    

def m2str(m):
    m_str = ""
    for k,v in m.items():
        m_str += k+": {:.4f}, ".format(v)
    
    return m_str
    

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
    las = avg_round(las)
#    vid = las
#    vidlas = np.round((vid + las) /2)
    


    #print(len(gt), len(vid))
    print("shape gt: {0}, shape vid: {1}".format(
                                                np.shape(gt),
                                                np.shape(vid)
    
                                                ))

    scores = []
    best_score = 0

    # Best results offset 45 for video, 55 for laser

    gt_temp = gt[45:]
    vid_temp = vid[0:-45]
    las_temp = las[0:-45]

    gt_temp = gt_temp[10:]
    vid_temp = vid_temp[0:-10]
    las_temp = las_temp[0:-10]

    # Merging approaches
    #vl_avg_1 = np.round((vid_temp + las_temp) /2)
    vl_avg_1 = np.mean(np.stack((vid_temp,las_temp)), axis=0)
    vl_max_1 = np.max(np.stack((vid_temp,las_temp)), axis=0)
    print(np.shape(vid_temp), np.shape(las_temp.T))
    print(np.shape(vl_max_1))

    # evaluation
    evaluate_results(vid_temp, gt_temp, 30, "v30")
    evaluate_results(las_temp, gt_temp, 30, "l30")
    evaluate_results(vl_avg_1, gt_temp, 30, "vl_avg_1_30")
    evaluate_results(vl_max_1, gt_temp, 30, "vl_max_1_30")
    evaluate_results_f(vid_temp, las_temp, gt_temp, 30, "avg", "vl_f_avg_30")
    evaluate_results_f(vid_temp, las_temp, gt_temp, 30, "max", "vl_f_max_30")
#    evaluate_results(vid_temp, gt_temp, 30, "v30")
    exit()

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
            
            gt_fb = get_flow_bin(gt_c_rs,90)
            vid_fb = get_flow_bin(vid_c_rs,90)

    #        print("NEW SHAPE ", np.shape(vid_c_rs))
            
    #        print(vid_c_rs)
            
#            score = compare_gt (vid_c_rs,gt_c_rs)
#            score = compare_detections (gt=gt_temp, res=vid_temp)
#            score = compare_detections (gt=gt_fb, res=vid_fb)
            score = compare_bool(gt=gt_fb, res=vid_fb)
            metrics = get_metrics(score)
            curr_score = metrics["TPR"] 
            
            if best_score < curr_score:
                best_score = curr_score
                print("BEST NEW= ", metrics, score, i, j)
            
            scores.append(curr_score)
        
        

    print("Best score", np.max(score))
    exit()


