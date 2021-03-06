# coding=utf8

import sys
import math
import datetime


# {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
#  'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
#  'The Night Listener': 3.0},
# 'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
#  'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
#  'You, Me and Dupree': 3.5},
# 'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
#  'Superman Returns': 3.5, 'The Night Listener': 4.0},
# 'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
#  'The Night Listener': 4.5, 'Superman Returns': 4.0,
#  'You, Me and Dupree': 2.5},
# 'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
#  'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
#  'You, Me and Dupree': 2.0},
# 'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
#  'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
# 'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


class item_based_cf:
    def __init__( self ):
        # 943users,1842movies,10w ratings
        # 3900users,6040movies,100w ratings
        # 71567users,10681movies,1000w ratings
        self.movie_path = "/home/xiaowei/data/movies.dat"
        self.rating_path = "/home/xiaowei/data/ratings.dat"
#         self.user_dict= {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
#  'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
#  'The Night Listener': 3.0},
# 'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
#  'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
#  'You, Me and Dupree': 3.5},
# 'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
#  'Superman Returns': 3.5, 'The Night Listener': 4.0},
# 'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
#  'The Night Listener': 4.5, 'Superman Returns': 4.0,
#  'You, Me and Dupree': 2.5},
# 'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
#  'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
#  'You, Me and Dupree': 2.0},
# 'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
#  'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
# 'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}
        self.user_dict = self.loadMoviesMid()
        self.item_dict = self.transformPrefs( self.user_dict )


    # dict transform
    def transformPrefs( self, prefs ):
        result = {}
        for person in prefs:
            for item in prefs[person]:
                result.setdefault( item, {} )
                result[item][person] = prefs[person][item]

        return result

    # calculate item similarity
    def calculateSimilarItems( self, prefs, n = 10 ):
        result = {}
        # 构造一个以物品为中心的字典
        itemsPrefs = self.transformPrefs( prefs )
        c = 0
        for item in itemsPrefs:
            c += 1
            if c % 100 == 0:
                print "%d/%d" % ( c, len( itemsPrefs ) )
            scores = self.topMatches( itemsPrefs, item, n = n, similarity = self.sim_distance )
            result[item] = scores
        return result

    def loadMoviesMid( self ):
        movies = {}
        # get movie titles
        for line in open( self.movie_path ):
            ( m_id, title ) = line.split( '::' )[0:2]
            movies[m_id] = title
        prefs = {}
        for line in open( self.rating_path ):
            ( user_id, movie_id, ratings ) = line.split( '::' )[0:3]
            prefs.setdefault( user_id, {} )
            prefs[user_id][movies[movie_id]] = float( ratings )
        return prefs

# if two samples has same property,calculate the Euclidean distance,use 1.0/(1+math.sqrt(sum_of_squares) to calculate similarity
# if the similarity is close to 1,means the two samples are similar
    def sim_distance( self, prefs, p1, p2 ):
        si = {}
        for item in prefs[p1]:
            if item in prefs[p2]:
                si[item] = 1

        if len( si ) == 0:
            return 0

        sum_of_squares = sum( [pow( prefs[p1][item] - prefs[p2][item], 2 ) for item in prefs[p1] if item in prefs[p2]] )
        # 书上用来测试的实例没有加上sqrt(sum_of_squares),虽然也没关系，不过user_based算法加了,只能当它是一个bug了...
        return 1.0 / ( 1 + ( sum_of_squares ) )

    # calculate the Pearson coefficient
    # if Pearson is close to 1,means the two samples are similar
    def sim_person( self, prefs, p1, p2 ):
        si = {}
        # 得到双方都评价过的物品列表
        for item in prefs[p1]:
            if item in prefs[p2]:
                si[item] = 1
        n = len( si )

        if n == 0:
            return 1

        sum1 = sum( [prefs[p1][it] for it in si] )
        sum2 = sum( [prefs[p2][it] for it in si] )

        sum1Sq = sum( [pow( prefs[p1][it], 2 ) for it in si] )
        sum2Sq = sum( [pow( prefs[p2][it], 2 ) for it in si] )

        psum = sum( [prefs[p1][it] * prefs[p2][it] for it in si] )

        # 计算皮尔逊评价值
        num = psum - ( sum1 * sum2 / n )
        den = math.sqrt( ( sum1Sq - pow( sum1, 2 ) / n ) * ( sum2Sq - pow( sum2, 2 ) / n ) )
        if den == 0:
            return 0

        r = num / den

        return r

    def getRecommendedItems( self, prefs, itemMatch, user ):
        userRatings = prefs[user]
        print userRatings
        scores = {}
        totalSim = {}

        for ( item, rating ) in userRatings.items():
            for ( similarity, item2 ) in itemMatch[item]:
                if item2 in userRatings:
                    continue

                # 评价值与相似度的加权之和
                scores.setdefault( item2, 0 )
                scores[item2] += similarity * rating

                # 全部相似度之和
                totalSim.setdefault( item2, 0 )
                totalSim[item2] += similarity

        rankings = [( score / totalSim[item], item ) for item, score in scores.items()]
        rankings.sort()
        rankings.reverse()

        return rankings

    def topMatches( self, prefs, person, n = 5, similarity = sim_distance ):
        scores = [( similarity( prefs, person, other ), other ) for other in prefs if other != person]
        scores.sort()
        scores.reverse()
        return scores[0:n]

if __name__ == '__main__':
    starttime = datetime.datetime.now()
    ib = item_based_cf()
#     itemsim=ib.calculateSimilarItems(ib.user_dict)
#     print ib.getRecommendedItems(ib.user_dict,itemsim, "Toby")
    itemsim = ib.calculateSimilarItems( ib.user_dict, n = 50 )
#     print itemsim
    print ib.getRecommendedItems( ib.user_dict, itemsim, "87" )
    endtime = datetime.datetime.now()
    interval = ( endtime - starttime ).seconds
    print "cost " + str( interval ) + " seconds"
