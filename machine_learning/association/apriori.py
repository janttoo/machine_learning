# coding=utf8
import sys
import os.path
import csv
import math
import types
from collections import defaultdict, Iterable
import itertools

class Apriori:
	def __init__(self, data, minSup, minConf):
		self.dataset = data
		# 事务集
		self.transList = defaultdict(list)
		# 频繁项集,value为出现频率
		self.freqList = defaultdict(int)
		# 项集
		self.itemset = set()
		# 所有事务集的数量
		self.numItems = 0
		# 初始化工作
		self.prepData()
		# 频繁k项集集合
		self.F = defaultdict(list)
		self.minSup = minSup
		self.minConf = minConf

	def genAssociations(self):
		candidate = {}
		count = {}
		# 传入参数是频繁项集
		# F[1]为频繁1-项集对应的item
		# Apriori采用支持度剪枝技术产生频繁项集
		self.F[1] = self.firstPass(self.freqList, 1)
#		print self.F[1],len(self.F[1]),len(self.freqList)
		k = 2
		while len(self.F[k - 1]) != 0:
			# 合并所有频繁(k-1)-项集,删除其组合后(k-1)-项集不是
			candidate[k] = self.candidateGen(self.F[k - 1], k)
			# 遍历事务集,key为行号,value为该行所有item
			# t-format (key,value)
			for t in self.transList.iteritems():
				for c in candidate[k]:
					#判断频繁候选项集支持度计数
					if set(c).issubset(t[1]):
						self.freqList[c] += 1

			#剪枝,少于支持度的全部剪掉
			self.F[k] = self.prune(candidate[k], k)
#			if k > 2:
#				self.removeSkyline(k, k - 1)
			k += 1
		return self.F

	def removeSkyline(self, k, kPrev):
		for item in self.F[k]:
			subsets = self.genSubsets(item)
			for subset in subsets:
				if subset in (self.F[kPrev]):
					self.F[kPrev].remove(subset)

		subsets = self.genSubsets

	def prune(self, items, k):
		f = []
		for item in items:
			count = self.freqList[item]
			support = self.support(count)
			if support >= self.minSup:
				f.append(item)
		return f

	# 产生候选项集
	# 蛮力，F[K-1]*F[1],F[k-1]*F[k-1]三种方法(数据挖掘导论P210)，这里是自创的一种..
	# 把所有的k-1频繁项集组合到一起,创造出k候选项集,然后删除该K候选集中所有的k-1候选集组合中不是频繁项集的选项
	def candidateGen(self, items, k):
		candidate = []
		if k == 2:
			# 会有(1,2),(1,2)这样的重复项
			candidate = [tuple(sorted([x, y])) for x in items for y in items if len((x, y)) == k and x != y]
		else:
			# 两个k-1的频繁项集并后,保证是k候选项集,后边再去删除掉所有的k-1子集不是频繁项的k候选集
			candidate = [tuple(sorted(set(x).union(y))) for x in items for y in items if len(set(x).union(y)) == k and x != y]

		candidate_copy = candidate[:]

		for c in candidate_copy:
			subsets = self.genLensets(c)
			if k==2:
				# k==2时,items里的每一个元素都为字符串，而subset里的元素都为元祖
				if any([ x[0] not in items for x in subsets ]):
					candidate.remove(c)
			else:
				if any([ x not in items for x in subsets ]):
					candidate.remove(c)
		return set(candidate)
	
	# 在item集合中找到所有len(item)-1的集合
	# input [1,2,3]
	# output [(1, 2), (1, 3), (2, 3)]
	def genLensets(self, item):
		subsets = []
		sublen = len(item)-1
		subsets.extend(itertools.combinations(item,sublen))
		return subsets
			
	# input [1,2,3]
	# output [(1,), (2,), (3,), (1, 2), (1, 3), (2, 3)]不包括(1,2,3)
	def genSubsets(self, item):
		subsets = []
		for i in range(1, len(item)):
			subsets.extend(itertools.combinations(item, i))
		return subsets

	def genRules(self, F):
		H = []
		for k, itemset in F.iteritems():
			if k >= 2:
				for item in itemset:
					subsets = self.genSubsets(item)
					for subset in subsets:
						if len(subset) == 1:
							subCount = self.freqList[subset[0]]
						else:
							subCount = self.freqList[subset]
						itemCount = self.freqList[item]
						if subCount != 0:
							confidence = self.confidence(subCount, itemCount)
							if confidence >= self.minConf:
								support = self.support(self.freqList[item])
								rhs = self.difference(item, subset)
								if len(rhs) == 1:
									H.append((subset, rhs, support, confidence))

		return H

	def difference(self, item, subset):
		return tuple(x for x in item if x not in subset)

	def confidence(self, subCount, itemCount):
		return float(itemCount) / subCount

	# 测试1-项集是否满足最小支持度
	def firstPass(self, items, k):
		f = []
		for item, count in items.iteritems():
			support = self.support(count)
			# item在所有项集中都存在,support==1
			if support >= self.minSup:
				f.append((item))
		return f

	def support(self, count):
		return float(count) / self.numItems

	def prepData(self):
		key = 0
		# 读入的文件,一行是一个购物篮,也就是一个事务
		for basket in self.dataset:
			# 所有事务的总和
			self.numItems += 1
			# 这里就是行号
			key = basket[0]
			for i, item in enumerate(basket):
				if i != 0:
					# 事务集,key为行号,value为该行所有item
					self.transList[key].append(item.strip())
					# 1-项集的所有记录，去重
					self.itemset.add(item.strip())
					# 1-项集记录的出现次数(支持度计数)
					self.freqList[(item.strip())] += 1

# 将item_id对应到实际的物品上
def readable(item, goods):
	itemStr = ""
	for k, i in enumerate(item):
		#k就是迭代次数从0开始,i是item_id,type=str
		itemStr += goods[i][0] + " " + goods[i][1] + " (" + i + ")"
		if len(item) != 0 and k != len(item) - 1:
			itemStr += ",\t"

	return itemStr.replace("'", "")

def main():
	goods = defaultdict(list)
	num_args = len(sys.argv)
	minSup = minConf = 0
	noRules = False

	# make sure the input format is right
	if num_args < 4 or num_args > 5:
		print 'Expected input format: python apriori.py <dataset.csv> <minSup> <minConf>'
		return
	elif num_args == 5 and sys.argv[1] == "--no-rules":
		dataset = csv.reader(open(sys.argv[2], "r"))
		#goods.csv包含50个货品和对应名称
		goodsData = csv.reader(open('/home/xiaowei/data/goods.csv', "r"))
		minSup = float(sys.argv[3])
		minConf = float(sys.argv[4])
		noRules = True
		print "Dataset:", sys.argv[2], "MinSup:", minSup, "MinConf:", minConf
	else:
		dataset = csv.reader(open(sys.argv[1], "r"))
		goodsData = csv.reader(open('/home/xiaowei/data/goods.csv', "r"))
		minSup = float(sys.argv[2])
		minConf = float(sys.argv[3])
		print "Dataset:", sys.argv[1], "MinSup:", minSup, "minConf:", minConf


	print "================================================================="
	for item in goodsData:
		# key为行号-1,value为4项
		goods[item[0]] = item[1:]

	# dataset format is linenum,item1,item2,item3
	a = Apriori(dataset, minSup, minConf)
	frequentItemsets = a.genAssociations()
	count = 0

	# k从1计数
	for k, item in frequentItemsets.iteritems():
		for i in item:
			#k>=2才涉及到关联,frequentItemsets的key为频繁项集的k
			if k >= 2:
				count += 1
				print count, ": ", readable(i, goods), "\t support=", a.support(a.freqList[i])


#	print "Skyline Itemsets: ", count
#
#	if not noRules:
#		rules = a.genRules(frequentItemsets)
#		for i, rule in enumerate(rules):
#			print "Rule", i + 1, ":\t ", readable(rule[0], goods), "\t-->", readable(rule[1], goods), "\t [sup=", rule[2], " conf=", rule[3], "]"
#
#	print "\n"


if __name__ == '__main__':
	main()
