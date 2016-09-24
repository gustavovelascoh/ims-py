import pickle
import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from sklearn.decomposition import PCA

def hough(x, y, m=100, n=181):
    phi = np.linspace(0, np.pi, n)
    p_vals = np.linspace(0, m-1, m)
    
    c_phi = np.cos(phi)
    s_phi = np.sin(phi)
    cx = np.dot(x,[c_phi])
    sy = np.dot(y,[s_phi])
    p = cx + sy
    
    pmin = np.min(p)
    pmax = np.max(p)
    
    pmax_1 = pmax - pmin
    
    p_im = np.zeros((m, n))
    #print("p_max = %s, p_min = %s" % (pmax, pmin))
    #print(p_vals)
    p_vals = p_vals*(pmax_1/(m-1))+pmin
    
    #print(p_vals)
    
    for row in p:
        col = 0
        for value in row:
            ind = int(np.round((value-pmin)*(m-1)/pmax_1))
            #print("ind,col %s" % ((ind,col),))
            try:
                p_im[ind,col] += 1
            except IndexError:
                ##print("p_im shape: %s" % (np.shape(p_im),))
                print("x,y: %s,%s" % (ind, col))
                #exit()
            col += 1
        #r_c = 0

    #print("P shape: %s" % (np.shape(p),))
    #print("PIM shape: %s" % (np.shape(p_im),))
    #p_im_max = np.max(p_im)
    #print("max p_im : %s " % (p_im_max))
    #print("pts >= 0.9*p_im_max %s " % (np.sum((p_im>0.9*p_im_max))))
    return (p_im, phi, p_vals,)
    
    
    

cwd = os.getcwd()

parser = argparse.ArgumentParser(description='Import cluster file')
parser.add_argument('file', metavar='file',
                    help='cluster file')
parser.add_argument('--features', action='store_true')
parser.add_argument('--noplot', action='store_true')

args = parser.parse_args()
#print("File: %s" % args.file)
#print("features: %s" % args.features)


#input_file = "00001_123578.clus"
#input_file = "00501_123578.clus"
#input_file = "01001_123578.clus"
#input_file = "01501_123578.clus"
#input_file = "02001_123578.clus"
input_file = "09501_123578.clus"

input_file = args.file

file = open(input_file, "rb")

#plt.ion()
if not args.noplot:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    fig.show()


clusters_data = pickle.load(file)

db = clusters_data["db"]
data = clusters_data["raw"]

core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_
print(db)
print(db.min_samples)
#print(db.core_sample_indices_)
#     exit()

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)



unique_labels = set(labels)
if not args.features:
    print('Estimated number of clusters: %d' % n_clusters_)
    print(unique_labels)
#colors = plt.cm.Jet(np.linspace(0, 1, len(unique_labels)))

colors = ['b', 'g', 'r', 'm']
colors+= colors+colors
colors+= colors+colors
colors+= colors+colors

colors_final = colors[0:len(unique_labels)]

for k, col in zip(unique_labels, colors_final):
    if k != -1:
        # Black used for noise.
        #col = 'k'

        class_member_mask = (labels == k)
        #print(sum(class_member_mask))
        
        has_lines = False
        
        if (sum(class_member_mask) >= db.min_samples):
            #pass
            #xy = data[class_member_mask & core_samples_mask]
            xy = data[class_member_mask]
            print("xy: %s" % xy)           
            bbox = [min(xy[:,0:1]), min(xy[:,1:2]),max(xy[:,0:1]), max(xy[:,1:2])]
            print("bbox: %s" % bbox)
            exit
            p_im, phi, p_vals = hough(xy[:,0:1], xy[:,1:2], 200, 361)

            p_im_max = np.max(p_im)
            print("max p_im : %s " % (p_im_max))
            num_max = np.sum((p_im>0.95*p_im_max))
            print("pts >= 0.9*p_im_max %s " % (num_max))
            
            
            
            if num_max <= 3:
                has_lines = True
                inds = np.where(p_im>0.95*p_im_max)
                print(inds)
                #if num_max > 1:
                    
                for x,y in zip(inds[0], inds[1]):
                    print("p,phi: %f,%f" % (p_vals[x],phi[y]))
                        #print("p,phi: %d,%d" % (p_vals[pair[0]], phi[pair[1]]))
                #else:
                    # print(inds)
                    #print("p,phi: %d,%d" % (p_vals[inds[0]], phi[inds[1]]))

            #plt.imshow(p_im,cmap="gray")
            #plt.show()            
            #input()
            #exit()
            
            
            f0 = np.shape(xy)
            f1 = xy.mean(axis=0)        
            f2 = xy.std(axis=0)
            f3 = scipy.stats.skew(xy,0)
            f4 = scipy.stats.kurtosis(xy,0)
            
            pca = PCA(n_components=2)
            pca.fit(xy)
            f5 = pca.explained_variance_ratio_
            
            output_str = ''
            
            if not args.features:
                output_str = str(k) + "\t"
            output_str += str(float(f0[0])) + "\t"
                
            #output_str += "\t".join(str(x) for x in f1) + "\t"
            output_str += "\t".join(str(x) for x in f2) + "\t"
            output_str += "\t".join(str(x) for x in f3) + "\t"
            output_str += "\t".join(str(x) for x in f4) + "\t"
            output_str += "\t".join(str(x) for x in f5)
            
            
            print(output_str)
            
            
            #print("Size data %s" % str(np.shape(data)))
            #print("Size xy %s" % str(np.shape(xy)))
            #print(xy)
            if not args.noplot:
                ax.plot(xy[:, 0], xy[:, 1], '.', markerfacecolor=col,
                         markeredgecolor='k', markersize=10)
            
                #xy = data[class_member_mask & ~core_samples_mask]
                #ax.plot(xy[:, 0], xy[:, 1], '.', markerfacecolor=col,
                #         markeredgecolor='k', markersize=4)
                
                ax.plot(f1[0], f1[1],marker='x', markersize=4)
                if has_lines:
                    ax.text(f1[0], f1[1], 'C' + str(k), color='r')
                else:
                    ax.text(f1[0], f1[1], 'C' + str(k))
                #input() 
                #exit()

if not args.noplot:
    plt.show()
    input()

