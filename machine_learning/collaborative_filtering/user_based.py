# coding=utf8
import sys
import math
import datetime

class user_based_cf:
    def __init__( self ):
        # ~/data/movies.dat ./data/ratings.dat  943 users,1842movies,10w ratings
        # ~/data/movies.dat1 ./data/ratings.dat1  13900users,6040movies,100w ratings
        # ~/data/movies.dat2  ./data/ratings.dat2  71567users,10681movies,1000w ratings
#         {'Lisa Rose':{'lady':2.5,'snakes':3.5,'just':3.0,'superman':3.5,'you':2.5,'the':3.0},
#         'Gene Seymour':{'lady':3.0,'snakes':3.5,'just':1.5,"superman":5.0,'the':3.0,'you':3.5},
#         'Michael Phillips':{'lady':2.5,'snakes':3.0,'superman':3.5,'the':4.0},
#         'Claudia Puig':{'snakes':3.5,'just':3.0,'the':4.5,'superman':4.0,'you':2.5},
#         'Mick LaSalle':{'lady':3.0,'snakes':4.0,'just':2.0,'superman':3.0,'the':3.0,'you':2.0},
#         'Jack Matthews':{'lady':3.0,'snakes':4.0,'the':3.0,'superman':5.0,'you':3.5},
#         'Toby':{'snakes':4.5,'you':1.0,'superman':4.0}}
        self.movie_path = "/home/xiaowei/data/movies.dat"
        self.rating_path = "/home/xiaowei/data/ratings.dat"
        self.prefs = self.loadMoviesMid()

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
    def sim_distance( self, p1, p2 ):
        si = {}
        for item in self.prefs[p1]:
            if item in self.prefs[p2]:
                si[item] = 1

        if len( si ) == 0:
            return 0

        sum_of_squares = sum( [pow( self.prefs[p1][item] - self.prefs[p2][item], 2 ) for item in si] )
        return 1.0 / ( 1 + math.sqrt( sum_of_squares ) )

    # calculate the Pearson coefficient
    # if Pearson is close to 1,means the two samples are similar
    def sim_pearson( self, p1, p2 ):
        si = {}
        # get the item list both p1 and p2 evaluated
        for item in self.prefs[p1]:
            if item in self.prefs[p2]:
                si[item] = 1
        n = len( si )

        if n == 0:
            return 1

        sum1 = sum( [self.prefs[p1][it] for it in si] )
        sum2 = sum( [self.prefs[p2][it] for it in si] )

        sum1Sq = sum( [pow( self.prefs[p1][it], 2 ) for it in si] )
        sum2Sq = sum( [pow( self.prefs[p2][it], 2 ) for it in si] )

        psum = sum( [self.prefs[p1][it] * self.prefs[p2][it] for it in si] )

        # Calculate pearson
        num = psum - ( sum1 * sum2 / n )
        den = math.sqrt( ( sum1Sq - pow( sum1, 2 ) / n ) * ( sum2Sq - pow( sum2, 2 ) / n ) )
        if den == 0:
            return 0

        r = num / den
        return r

    # get the Best matches n
    def topMatches( self, person, n = 5, similarity = sim_distance ):
        scores = [( similarity( self, person, other ), other ) for other in self.prefs if other != person]
        scores.sort()
        scores.reverse()
        return scores[0:n]


    # get recommend results
    def getRecommendations( self, person, similarity = sim_pearson ):
        totals = {}
        simSums = {}
        # not to compare its own

        for other in self.prefs:
            if other == person:
                continue

            # if Evaluation value<=0 not to compare
            sim = similarity( self, person, other )
            if sim <= 0:
                continue

            for item in self.prefs[other]:
                # find the best items,take care of simSum(the similar sum)
                if item not in self.prefs[person] or self.prefs[person][item] == 0:
                    totals.setdefault( item, 0 )
                    totals[item] += self.prefs[other][item] * sim
                    simSums.setdefault( item, 0 )
                    simSums[item] += sim

        ranking = [( total / simSums[item], item ) for item, total in totals.items()]
        ranking.sort()
        ranking.reverse()
        return ranking

if __name__ == '__main__':
    starttime = datetime.datetime.now()
    ub = user_based_cf()
#     print ub.prefs["87"]
    # [(5.0, 'They Made Me a Criminal (1939)'), (5.0, 'Star Kid (1997)'), (5.0, 'Santa with Muscles (1996)'), (5.0, 'Saint of Fort Washington, The (1993)'), (5.0, 'Marlene Dietrich: Shadow and Light (1996) '), (5.0, 'Great Day in Harlem, A (1994)'), (5.0, 'Entertaining Angels: The Dorothy Day Story (1996)'), (5.0, 'Boys, Les (1997)'), (4.89884443128923, 'Legal Deceit (1997)'), (4.815019082242709, 'Letter From Death Row, A (1998)'), (4.800260666069043, 'Mrs. Dalloway (1997)'), (4.771240079753504, 'Leading Man, The (1996)'), (4.7321082983941425, 'Hearts and Minds (1996)'), (4.707354190896574, 'Dangerous Beauty (1998)'), (4.696244466490867, 'Pather Panchali (1955)'), (4.652397061026758, 'Lamerica (1994)'), (4.532337612572981, 'Innocents, The (1961)'), (4.527998574747079, 'Casablanca (1942)'), (4.512903125553784, 'Four Days in September (1997)'), (4.510270149719864, 'Everest (1998)'), (4.485151301801342, 'Wallace & Gromit: The Best of Aardman Animation (1996)'), (4.463287461290222, 'Wrong Trousers, The (1993)'), (4.450979436941035, 'Kaspar Hauser (1993)'), (4.431079071179518, 'Usual Suspects, The (1995)'), (4.427520682864959, 'Maya Lin: A Strong Clear Vision (1994)'), (4.414870784592075, 'Wedding Gift, The (1994)'), (4.407740300866056, 'Duoluo tianshi (1995)'), (4.393353032192906, 'Close Shave, A (1995)'), (4.377445252656464, 'Affair to Remember, An (1957)'), (4.374146179500976, 'Anna (1996)')]
    print  ub.getRecommendations( "87" )[0:30]
    endtime = datetime.datetime.now()
    interval = float( ( endtime - starttime ).seconds )
    print "cost " + str( interval ) + " seconds"
