#coding=utf8

'''created on Sep 16th,2013
Contain example of knn
@author bianxiaowei   email :xiaowei_bian@163.com
DataSet http://archive.ics.uci.edu/ml/datasets/Yeast
1484 records,8 attrbutes'''

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split, cross_val_score

class RandomForest:
    '''
    Example of knn using dataset above
    '''
    #Predicted category mush be  numeric types
    #so yeast_target.dat format is:MIT 4,NUC 3
    def loadData(self):
        f_matrix=file("/home/xiaowei/data/yeast.dat","r")
        f_target=file("/home/xiaowei/data/yeast_target.dat","r")
        data=np.loadtxt(f_matrix)
        data=data.astype(np.float)
        labels=np.array([line.strip('\n').split(' ')[1] for line in f_target])
        labels=labels.astype(np.int)
        print "Load Data Finish"
        return data,labels
        
    def doWork(self,DataIn,LabelsIn):    
        forest=RandomForestClassifier(n_estimators=10, n_jobs=-1)        
        scores=cross_val_score(forest,DataIn,LabelsIn,cv=5)
        print "RandomForest Accuracy: %0.2f (+/- %0.3f)" % (scores.mean(),scores.std()*1.0/2)
        #split Data into trainData and testData   
        DataTrain,DataTest,LabelTrain,LabelTest=train_test_split(DataIn,LabelsIn,test_size=0.2,random_state=1) 
        forest.fit(DataTrain,LabelTrain)
        print "accuracy_rate",forest.score(DataTest,LabelTest)
    
if __name__=='__main__':
    RF=RandomForest()
    trainData,labels=RF.loadData()
    RF.doWork(trainData, labels)