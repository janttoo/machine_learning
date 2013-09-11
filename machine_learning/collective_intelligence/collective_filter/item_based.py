#coding=utf8

import sys
import math
import datetime

class item_based_cf:
    def __init__(self):
        #943用户,1842影片
        #3900用户,6040影片,100w ratings
        #71567用户,10681影片,1000w ratings
        self.movie_path="./data/movies.dat1"
        self.rating_path="./data/ratings.dat1"
        self.prefs=self.loadMoviesMid()

      #物品的相似度
    def calculateSimilarItems(self):
        result={}
        c=0
        for item in self.prefs:
            scores=self.topMatches(item)
            result[item]=scores
        return result   
    
    def loadMoviesMid(self):
        movies={}
        #获取影片标题
        for line in open(self.movie_path):
            (id,title)=line.split('::')[0:2]
            movies[id]=title
        prefs={}
        for line in open(self.rating_path):
            (user_id,movie_id,ratings)=line.split('::')[0:3]
            prefs.setdefault(movies[movie_id],{})
            prefs[movies[movie_id]][user_id]=float(ratings)
        return prefs
    
#计算拥有同种属性的欧式距离,然后利用1.0/(1+sqrt(sum))计算相似度
    #相似度越接近1，说明两个样本越相近
    def sim_distance(self,p1,p2):
        si={}
        for item in self.prefs[p1]:
            if item in self.prefs[p2]:
                si[item]=1
                
        if len(si)==0:
            return 0
    
        sum_of_squares=sum([pow(self.prefs[p1][item]-self.prefs[p2][item],2) for item in si])
        return 1.0/(1+math.sqrt(sum_of_squares))
    
    #返回p1和p2的皮尔逊系数
    #皮尔逊系数越接近1，说明两个样本越相近
    def sim_pearson(self,p1,p2):
        si={}
        #得到双方都评价过的物品列表
        for item in self.prefs[p1]:
            if item in self.prefs[p2]:
                si[item]=1
        n=len(si)
    
        if n==0:
            return 1
    
        sum1=sum([self.prefs[p1][it] for it in si])
        sum2=sum([self.prefs[p2][it] for it in si])
    
        sum1Sq=sum([pow(self.prefs[p1][it],2) for it in si])
        sum2Sq=sum([pow(self.prefs[p2][it],2) for it in si])
    
        psum=sum([self.prefs[p1][it]*self.prefs[p2][it] for it in si])
    
        #计算皮尔逊评价值
        num=psum-(sum1*sum2/n)
        den=math.sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
        if den==0:
            return 0
    
        r=num/den
        return r    
    
    #从反映偏好的字典中返回最为匹配者
    #返回结果的个数和相似度函数均为可选参数
    def topMatches(self,person,n=3,similarity=sim_pearson):
        scores=[(similarity(self,person,other),other) for other in self.prefs if other!=person]
        scores.sort()
        scores.reverse()
        return scores[0:n]
    
    #利用所有他人评价值的加权平均，为某人提供建议
    def getRecommendations(self,person,similarity=sim_pearson):
        totals={}
        simSums={}
        #不和自己做比较
        for other in self.prefs:
            if other==person:
                continue
    
            #评价值为0或是小于0不作比较
            sim=similarity(self,person,other)
            if sim<=0:
                continue
    
            for item in self.prefs[other]:
                #在别人看过的item中，找到自己没有看过的item
                if item not in self.prefs[person] or self.prefs[person][item]==0:
                    totals.setdefault(item,0)
                    totals[item]+=self.prefs[other][item]*sim
                    simSums.setdefault(item,0)
                    totals[item]+=self.prefs[other][item]*sim
                    simSums.setdefault(item,0)
                    simSums[item]+=sim
    
    
        ranking=[(total/simSums[item],item) for item,total in totals.items()]
        ranking.sort()
        ranking.reverse()
        return ranking
    
    
if __name__=='__main__':
    starttime=datetime.datetime.now()
    ib=item_based_cf()
    print "hehe"
    print ib.calculateSimilarItems()[0:5]
    print "abc"
    print  ib.getRecommendations("Toy Story (1995)")[0:5]
    print "all ok"
    endtime=datetime.datetime.now()
    interval=(endtime-starttime).seconds
    print "cost "+str(interval)+" seconds"