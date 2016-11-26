from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
import argparse
import os
from scipy.cluster.vq import vq, kmeans, whiten
from sklearn.cluster import KMeans as sk_kmeans
import pickle

cwd = os.getcwd()

parser = argparse.ArgumentParser(description='Feature Analyisis')
parser.add_argument('action', metavar='action',
                    help='action to perform (dendogram, kmeans3, kmeans4)')

args = parser.parse_args()
features = np.loadtxt("cluster_features", delimiter=",")

if args.action == "dendogram":
    
    
    print(np.shape(features))
    
    
    Z = linkage(features, 'ward')
    
    from scipy.cluster.hierarchy import cophenet
    from scipy.spatial.distance import pdist
    
    c, coph_dists = cophenet(Z, pdist(features))
    print(c)
    
    # calculate full dendrogram
    plt.figure(figsize=(25, 10))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
    )
    plt.show()
elif args.action == "kmeans3":
    data={}
    data["std"] = np.std(features, axis=0)
    print()
    whitened = whiten(features)
    book = np.array((whitened[0],whitened[2]))
    np.random.seed((1300,2000))
    codes = 3
    k1 = kmeans(whitened,codes)
    k2 = sk_kmeans(n_clusters=2 )
    k2.fit(whitened)
    k2.cluster_centers_
    
    print("k1: %s, %s" % (k1))
    print("k2: %s" % (k2.cluster_centers_))
    
    print("Feats[0:3]: %s" % features[0:3])
    
    print(k2.labels_)
    data["model"] = k2
    fo = open("kmeans3_sk.model", "wb")
    pickle.dump(data, fo, pickle.HIGHEST_PROTOCOL)
    
    
    pass
elif args.action == "kmeans4":
    pass
elif args.action == "PCA":
    pass
elif args.action == "plot":
    s,f = np.shape(features)
    print("shape %s,%s" % (s, f))
    
    fig, ax = plt.subplots(f-1, f-1)
    
    #print(features[:,12])
    #print(ax)
    
    for i in range(0, f-1):
        row=''
        for j in range(i+1, f-1):
            row+='%s,%s\t' % (i,j)
            ax[i,j].plot(features[:,i],features[:,j],'. ')
            
        print(row)
        
    plt.show()
            
    
    
    pass
else:
    print("Invalid action")