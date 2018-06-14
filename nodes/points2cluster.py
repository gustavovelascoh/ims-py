'''
Created on Jun 12, 2018

@author: gustavo
'''
import json
import time
import numpy as np
from sklearn.cluster import DBSCAN
from models.subscriber import Subscriber


class Points2Clusters():
    def __init__(self, in_ch="", out_ch=""):
        self.dbscan_params = {'eps':0.3, 'min_samples':5}
        self.out_ch = out_ch
        self.s= Subscriber({in_ch: self.__points_msg_cb})
        
        self.s.run()
    
    def __points_msg_cb(self,msg):
        data_str = msg["data"].decode("utf-8")
        data = json.loads(data_str)
                
        xydata = np.array([data["x"],data["y"]]).transpose()
        
        clusters_msg = {}
        clusters_msg["ts"] = data["ts"]
        clusters_dict = self.get_clusters(xydata)
        clusters_msg["data"] = clusters_dict["list"]
        clusters_msg["n_clusters"] = clusters_dict["n_clusters"]
        clusters_msg["curr_ts"] = time.time()
        #print(clusters_msg)
        self.s.r.publish(self.out_ch, json.dumps(clusters_msg))
    
    def get_clusters(self, xydata):
        
        db = DBSCAN(**self.dbscan_params).fit(xydata/100.0)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_
        
        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        
        clusters_msg = {}        
        clusters_msg["n_clusters"] = n_clusters_
        clusters_msg["list"] = [] 
        unique_labels = set(labels)
        
        
        for k in unique_labels:
            if k != -1:
                class_member_mask = (labels == k)
                
                if (sum(class_member_mask) >= db.min_samples):
                    clus_data = xydata[class_member_mask]
                    clus_msg = {"x": clus_data[:,0].tolist(),
                                "y": clus_data[:,1].tolist(),
                                "id": int(k)}
                    clusters_msg["list"].append(clus_msg)
        #print(xydata)
        return clusters_msg
    
if __name__ == "__main__":
    
    import argparse
    
    description_str='Subscribe to cartesian data and find clusters'
    parser = argparse.ArgumentParser(description=description_str)
    parser.add_argument('ich',
                        metavar='ICH',
                        help="Input channel")
    parser.add_argument('och',
                        metavar='OCH',
                        help="Output channel")
    args = parser.parse_args()
    
    p2c = Points2Clusters(in_ch=args.ich, out_ch=args.och)
    
    
