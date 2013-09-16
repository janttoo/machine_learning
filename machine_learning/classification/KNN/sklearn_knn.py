#coding=utf8

'''created on Sep 16th,2013
Contain example of knn
@author bianxiaowei   email :xiaowei_bian@163.com
DataSet http://archive.ics.uci.edu/ml/datasets/Yeast
1484 records,8 attrbutes'''

import numpy as np
from sklearn.neighbors import KNeighborsClassifier

class Knn:
    '''
    Example of knn using dataset above
    '''

    #Predicted category mush be  numeric types
    #so yeast_target.dat format is:MIT 4,NUC 3
    def loadData(self):
        f_matrix=file("./yeast.dat","r")
        f_target=file("./yeast_target.dat","r")
        data=np.loadtxt(f_matrix)
        labels=[line.strip('\n').split(' ')[1] for line in f_target]
        print "Load Data Finish"
        return data,labels
    
    def doWork(self,trainData,labels):       
        neigh=KNeighborsClassifier (n_neighbors=3,algorithm="kd_tree")
        neigh.fit(trainData,labels)
        print "Train Data Finish"
        print neigh.predict([0.58 ,0.44,  0.57,  0.13 , 0.50 , 0.00 , 0.54 , 0.22])
    
    def writetoFile(self):
        f=file("knn_output.txt","w")
        
if __name__=='__main__':
    knn=Knn()
    trainData,labels=knn.loadData()
    neigh=knn.doWork(trainData, labels)
   
