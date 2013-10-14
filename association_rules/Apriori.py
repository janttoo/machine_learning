#coding=utf8

import sys
import os
import csv
import math
from collections import defaultdict, Iterable
import itertools
from optparse import OptionParser, OptParseError

class Apriori:
    def __init__(self,data,minSup,minConf):
        self.dataset=data                   #列表
        self.numItems=0                     #事务集总数 
        self.minSup=minSup
        self.minConf=minConf
        self.itemset=set()
        self.F=defaultdict(list)            #第一步的频繁项集
        self.freqList=defaultdict(int)      #支持度计数
        self.tranList=defaultdict(list)
        self.dataInit()
    
    #初始化数据，产生频繁子集F
    def dataInit(self):
        key=0
        for basket in self.dataset:
            self.numItems+=1
            key=basket[0]
            for i,item in enumerate(basket):
                if i!=0:
                    self.tranList[key].append(item.strip())
                    self.itemset.add(item.strip())
                    self.freqList[(item.strip())]+=1
                    
    #产生频繁项集F
    def frequentItemsGenerate(self):
        candidate={}
        self.F[1]=self.findFirstPass(self.freqList,1)
        k=2
        while len(self.F[k-1]):
            candidate[k]=self.aprioriGen(self.F[k-1],k)
            for t in self.tranList.iteritems():          
                for c in candidate[k]:
                    if set(c).issubset(t[1]):
                        self.freqList[c]+=1
                                    
            self.F[k]=self.prune(candidate[k],k)
#             print self.F[k],k
            k+=1
            
        return self.F
     
    def support(self,count):
        return float(count)/self.numItems
     
    def findFirstPass(self,items,k):
        f=[]
        for item,count in items.iteritems():
            support=self.support(count)
            if support>=self.minSup:
                f.append(tuple(item))
        return f
                    
    def aprioriGen(self,items,k):
        candidate = []
        if k==2:
            candidate = list(set([tuple(sorted(set(x).union(y))) for x in items for y in items if len((x,y))==k and x!=y]))
        else:
            candidate = list(set([tuple(sorted(set(x).union(y))) for x in items for y in items if x[:-1]==y[:-1] and x[-1]!=y[-1] and len(set(x).union(y))==k]))
        return candidate
    
    def prune(self,items,k):
        f=[]
        for item in items:
            count=self.freqList[item]
            support=self.support(count)
            if support>=self.minSup:
                f.append(item)
        return f
    
    #所有的子项
    def genSubsets(self,item):
        subsets = []
        for i in range(1,len(item)):
            subsets.extend(itertools.combinations(item,i))
        return subsets
    
    def confidence(self,subCount,itemCount):
        return float(subCount)/float(itemCount)
    
    def ruleGenerate(self,F):
        H=[]
        for k,itemset in F.iteritems():
            if k>=2:
                for item in itemset:
                    subsets=self.genSubsets(item)
                    for subset in subsets:
                        subCount=self.freqList[subset]
                        itemCount=self.freqList[item]
                        if subCount != 0:
                            support = self.support( self.freqList[item] )
                            confidence = self.confidence(subCount,itemCount)
                            if confidence>=self.minConf:
                                ruleTarget=self.difference(item,subset)
                                if len(ruleTarget)==1 and len(subset)>1:
                                    H.append((subset,ruleTarget,support,confidence))
        return H
    
   
    def difference( self, item, subset ):
        return tuple( x for x in item if x not in subset )

def readable(item,goods):
    itemStr = ""
    for k, i in enumerate( item ):
        # k就是迭代次数从0开始,i是item_id,type=str
        itemStr += goods[i][0] + " " + goods[i][1] + " (" + i + ")"

        if len( item ) != 0 and k != len( item ) - 1:
            itemStr += ",\t"

    return itemStr.replace( "'", "" )
    
def main():
    optparser=OptionParser()
    optparser.add_option('-f','--inputFile',dest="input",help="the file which contains the comma seperated value")
    optparser.add_option('-s','--minsupport',dest="minSup",help="minimum support value",default=0.5,type=float)
    optparser.add_option('-c','--minConfindence',dest="minConf",help="minimum confidence value",default=0.6,type=float)
    
    (options,args) = optparser.parse_args()
    
    inFile=None
    if options.input is None:
        inFile=sys.stdin
    elif options.input is not None:
        inFile=csv.reader(open("apriori-dataset.csv","r"))
    else:
        print "No dataset filename specified,system will exit\n"
        sys.exit("system will exit")
        
    minSupport=options.minSup
    minConfidence=options.minConf
    a=Apriori(inFile,minSupport,minConfidence)
    
    freqItems=a.frequentItemsGenerate()
    rules=a.ruleGenerate(freqItems)
    goodsData = csv.reader( open( './apriori-goods.csv', 'r' ) )
    goods=defaultdict(list)
    for item in goodsData:
        goods[item[0]] = item[1:]

    # k从1计数
    for i, rule in enumerate( rules ):
        print "Rule", i + 1, ":\t ", readable( rule[0], goods ), "\t-->", readable( rule[1], goods ), "\t [sup=", rule[2], " conf=", rule[3], "]"
   
if __name__=='__main__':
    main()
