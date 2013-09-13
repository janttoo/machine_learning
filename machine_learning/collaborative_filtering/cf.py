#!/usr/bin/env python
#coding=utf8
import sys
import math
import logging

#二维字典转换
def transformPrefs(prefs):
	result={}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item,{})
			result[item][person]=prefs[person][item]

	return result

#计算拥有同种属性的欧式距离,然后利用1.0/(1+sqrt(sum))计算相似度
#相似度越接近1，说明两个样本越相近
def sim_distance(prefs,p1,p2):
	si={}
	for item in prefs[p1]:
		if item in prefs[p2]:
			si[item]=1

	if len(si)==0:
		return 0

	sum_of_squares=sum([pow(prefs[p1][item]-prefs[p2][item],2) for item in si])
	return 1.0/(1+math.sqrt(sum_of_squares))


#返回p1和p2的皮尔逊系数
#皮尔逊系数越接近1，说明两个样本越相近
def sim_person(prefs,p1,p2):
	si={}
	#得到双方都评价过的物品列表
	for item in prefs[p1]:
		if item in prefs[p2]:
			si[item]=1
	n=len(si)

	if n==0:
		return 1

	sum1=sum([prefs[p1][it] for it in si])
	sum2=sum([prefs[p2][it] for it in si])

	sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
	sum2Sq=sum([pow(prefs[p2][it],2) for it in si])

	psum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

	#计算皮尔逊评价值
	num=psum-(sum1*sum2/n)
	den=math.sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
	if den==0:
		return 0

	r=num/den

	return r

#从反映偏好的字典中返回最为匹配者
#返回结果的个数和相似度函数均为可选参数
def topMatches(prefs,person,n=5,similarity=sim_distance):
	scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]		
	scores.sort()
	scores.reverse()
	return scores[0:n]

#利用所有他人评价值的加权平均，为某人提供建议
def getRecommendations(prefs,person,similarity=sim_person):
	totals={}
	simSums={}
	#不和自己做比较
	for other in prefs:
		if other==person:
			continue

		#评价值为0或是小于0不作比较
		sim=similarity(prefs,person,other)
		if sim<=0:
			continue

		for item in prefs[other]:
			#在别人看过的item中，找到自己没有看过的item
			if item not in prefs[person] or prefs[person][item]==0:
				totals.setdefault(item,0)
				totals[item]+=prefs[other][item]*sim
				simSums.setdefault(item,0)
				totals[item]+=prefs[other][item]*sim
				simSums.setdefault(item,0)
				simSums[item]+=sim


	ranking=[(total/simSums[item],item) for item,total in totals.items()]
	ranking.sort()
	ranking.reverse()
	return ranking


#物品的相似度
def calculateSimilarItems(prefs):
	result={}
	itemsPrefs=transformPrefs(prefs)
	c=0
	for item in itemsPrefs:
		c+=1
		if c%100==0:
			print "%d/%d" %(c,len(itemsPrefs))
		scores=topMatches(itemsPrefs,item,n=5,similarity=sim_distance)
		result[item]=scores
	return result

#读取数据集
def loadMovies(path="./data/"):
	movies={}
	#获取影片标题
	for line in open(path+'u.item'):
		(id,title)=line.split('|')[0:2]
		movies[id]=title
	#加载数据
	prefs={}
	for line in open(path+'u.data'):
		(user,movieid,rating,ts)=line.split('\t')
		prefs.setdefault(user,{})
		prefs[user][movies[movieid]]=float(rating)
	return prefs

if __name__=='__main__':
	p_dict=loadMovies()
# 	print p_dict['87']
	print calculateSimilarItems(p_dict)
# 	print getRecommendations(p_dict,'87')
