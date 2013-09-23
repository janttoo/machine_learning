#coding=utf8
import sys
import os.path
import csv
import math
import types
from collections import defaultdict,Iterable
import itertools

class Apriori:
    def __init__(self,data,minSup,minConf):
        self.dataset=data
        self.transList=defaultdict(list)
        self.freqList=defaultdict(list)
        #项集
        self.itemset=set()
        #频繁项集
        self.highSupportList=list()
        self.numItems=0
        #初始化工作
        self.prepData()
        self.F=defaultdict(list)
        self.minSup=minSup
        self.minConf=minConf
        
    def prepData(self):
        key=0
        for basket in self.dataset:
            self.numItems+=1
            key=basket[0]
            
def main():
    good=defaultdict(list)
    num_args=len(sys.argv)
    minSup=minConf=0
    noRules=False
    
    #Make sure the right number of input files are specified
    if num_args<4 or num_args>5:
        print 'Expected input format: python apriori.py <dataset.csv> <minSup> <minConf>'
        return
    elif num_args==5 and sys.argv[1]=="--no-rules":
        dataset=csv.reader(open(sys.argv[2],"r"))
        minSup=float(sys.argv[3])
        minConf=float(sys.argv[4])
        noRules=True
        print "Dataset:",sys.argv[2],"MinSup:",minSup,"MinConf:",minConf
    else:
        dataset=csv.reader(open(sys.argv[1],"r"))
        goodsData=csv.reader(open('goods.csv',"r"))
        minSup=float(sys.argv[2])
        minConf=float(sys.argv[3])
        print "Dataset:",sys.argv[1],"MinSup:",minSup,"minConf:",minConf
        
    print "===================================================="
    
    for item in goodsData:
        goodsData=
        
        
        
        
        
    
    
    
    
    
    
    
    
if __name__=='__main__':