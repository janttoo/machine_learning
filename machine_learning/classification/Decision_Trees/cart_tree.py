# coding=utf8
'''created on Sep 17th,2013
Contain example of CART(Classification and Regression Trees,分类回归树)
DataSet:http://archive.ics.uci.edu/ml/machine-learning-databases/car/
@author bianxiaowei   email :xiaowei_bian@163.com
1728 records,6 attributes
'''
from PIL import Image, ImageDraw
my_data = []

# col待检验的判断条件对应的列索引值
# value对应于为了使结果为true，当前列必须匹配的值
# tb和fb也是decisionnode，他们对应于结果分别为true或false时，树上相对于当前节点的子树上的节点
# results保存的是针对于当前分支的结果，除叶节点歪，在其他节点上该值都为None
class decisionnode:
    def __init__( self, col = -1, value = None, results = None, tb = None, fb = None ):
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb

def loadLocalData():
    global my_data
    my_data = [line.strip( '\n' ).split( '\t' ) for line in file( './tree_data.txt' )]

def loadCarData():
    global my_data
    my_data = [line.strip( '\n' ).split( ',' ) for line in file( '/home/xiaowei/data/car.dat' )]
#     my_data=my_data[0:100]

def loadIrisData():
    global my_data
    my_data = [line.strip( '\n' ).split( ',' ) for line in file( '/home/xiaowei/data/iris.dat' )]


def divideset( rows, column, value ):
    split_function = None
    if isinstance( value, int ) or isinstance( value, float ):
        split_function = lambda row:row[column] >= value
    else:
        split_function = lambda row:row[column] == value

    set1 = [row for row in rows if split_function( row )]
    set2 = [row for row in rows if not split_function( row )]

    return ( set1, set2 )

# 对各种可能的结果进行计数
def uniquecounts( rows ):
    results = {}
    for row in rows:
        # 计数结果在最后一列
        r = row[len( row ) - 1]
        if r not in results:
            results[r] = 0
        results[r] += 1
    return results

# 随机放置的数据项出现于错误分类中的概率
def giniimpurity( rows ):
    total = len( rows )
    counts = uniquecounts( rows )
    imp = 0
    for k1 in counts:
        p1 = float( counts[k1] ) / total
        for k2 in counts:
            if k1 == k2:
                continue
            p2 = float( counts[k2] ) / total
            imp += p1 * p2
    return imp

# 熵是遍历所有可能的结果之后所得到的p(x)log(p(x))之和
# 群组越混乱，熵的值越高
def entropy( rows ):
    from math import log
    log2 = lambda x:log( x ) / log( 2 )
    results = uniquecounts( rows )
    ent = 0.0
    for r in results.keys():
        p = float( results[r] ) / len( rows )
        ent = ent - p * log2( p )
    return ent

def buildtree( rows, scoref = entropy ):
    if len( rows ) == 0:
        return decisionnode()
    # 全局熵值
    current_score = scoref( rows )

    # 定义一些变量来记录最佳拆分条件
    best_gain = 0.0
    best_criteria = None
    best_sets = None

    # 遍历每一列，最后一列是用来存放分类结果的，因此不需要，只要前面的就好了
    column_count = len( rows[0] ) - 1

    for col in range( 0, column_count ):
        column_values = {}
        for row in rows:
            # 每次只装载一列的信息
            column_values[row[col]] = 1
        # 这一列的每个值，对数据集进行拆分
        for value in column_values.keys():
            ( set1, set2 ) = divideset( rows, col, value )

            p = float( len( set1 ) ) / len( rows )
            # 选择信息增益最大的，增益大，说明分类后的结果的熵值小，说明分类后的结果混乱程序小
            gain = current_score - p * scoref( set1 ) - ( 1 - p ) * scoref( set2 )
            if best_gain < gain and len( set1 ) > 0 and len( set2 ) > 0:
                best_gain = gain
                best_criteria = ( col, value )
                best_sets = ( set1, set2 )


    if best_gain > 0:
        trueBranch = buildtree( best_sets[0] )
        falseBranch = buildtree( best_sets[1] )
        return decisionnode( col = best_criteria[0], value = best_criteria[1], tb = trueBranch, fb = falseBranch )
    # 熵值最低的一对子集求得的加权平均熵比当前集合的熵要大，拆分过程就结束了
    else:
        return decisionnode( results = uniquecounts( rows ) )


def printtree( tree, indent = '' ):
    if tree.results != None:
        print str( tree.results )
    else:
        print str( tree.col ) + ':' + str( tree.value ) + '?'
        # 打印分支
        print indent + 'T->',
        printtree( tree.tb, indent + ' ' )
        print indent + 'F->',
        printtree( tree.fb, indent + ' ' )

def getwidth( tree ):
    if tree.tb == None and tree.fb == None:
        return 1
    return getwidth( tree.tb ) + getwidth( tree.fb )

def getdepth( tree ):
    if tree.tb == None and tree.fb == None:
        return 0
    return max( getdepth( tree.tb ), getdepth( tree.fb ) ) + 1

def drawtree( tree, jpeg = "tree.jpg" ):
    w = getwidth( tree ) * 200
    h = getdepth( tree ) * 100 + 120

    img = Image.new( 'RGB', ( w, h ), ( 255, 255, 255 ) )
    draw = ImageDraw.Draw( img )

    drawnode( draw, tree, w / 2, 40 )
    img.save( jpeg, 'JPEG' )

    drawnode( draw, tree, w / 2, 40 )
    img.save( jpeg, 'JPEG' )
    img.show()

def drawnode( draw, tree, x, y ):
    if tree.results == None:
        w1 = getwidth( tree.fb ) * 100
        w2 = getwidth( tree.tb ) * 100

        left = x - ( w1 + w2 ) / 2
        right = x + ( w1 + w2 ) / 2
        draw.text( ( x - 20, y - 10 ), str( tree.col ) + ':' + str( tree.value ), ( 0, 0, 0 ) )
        draw.line( ( x, y, left + w1 / 2, y + 100 ), fill = ( 255, 0, 0 ) )
        draw.line( ( x, y, right - w2 / 2, y + 100 ), fill = ( 255, 0, 0 ) )

        drawnode( draw, tree.fb, left + w1 / 2, y + 100 )
        drawnode( draw, tree.tb, right - w2 / 2, y + 100 )
    else:
        txt = ' \n'.join( ['%s:%d' % v for v in tree.results.items()] )
        draw.text( ( x - 20, y ), txt, ( 0, 0, 0 ) )


def classify( observation, tree ):
    if tree.results != None:
        return tree.results
    else:
        v = observation[tree.col]
        branch = None
        if isinstance( v, int ) or isinstance( v, float ):
            if v >= tree.value:
                branch = tree.tb
            else:
                branch = tree.fb
        else:
            if v == tree.value:
                branch = tree.tb
            else:
                branch = tree.fb
    return classify( observation, branch )

# mingain是合并时的参数，是否熵值得差小于这个数值
def prune( tree, mingain ):
    if tree.tb.results == None:
        prune( tree.tb, mingain )
    if tree.fb.results == None:
        prune( tree.fb, mingain )

    if tree.tb.results != None and tree.fb.results != None:
        tb, fb = [], []
        for v, c in tree.tb.results.items():
            tb += [[v]] * c
        for v, c in tree.fb.results.items():
            fb += [[v]] * c


        delta = entropy( tb + fb ) - ( entropy( tb ) + entropy( fb ) ) / 2
        if delta < mingain:
            tree.tb, tree.fb = None, None
            tree.results = uniquecounts( tb + fb )

# 处理缺失数据
def mdclassify( observation, tree ):
    if tree.results != None:
        return tree.results
    else:
        v = observation[tree.col]
        if v == None:
            tr, fr = mdclassify( observation, tree.tb ), mdclassify( observation, tree.fb )
            tcount = sum( tr.values() )
            fcount = sum( fr.values() )
            tw = float( tcount ) / ( tcount + fcount )
            fw = float( fcount ) / ( tcount + fcount )

            result = {}
            for k, v in tr.items():
                result[k] = v * tw
            for k, v in fr.items():
                if k not in result:
                    result[k] = 0
                result[k] += v * fw
            return result
        else:
            if isinstance( v, int ) or isinstance( v, float ):
                if v >= tree.value:
                    branch = tree.tb
                else:
                    branch = tree.fb
            else:
                if v == tree.value:
                    branch = tree.tb
                else:
                    branch = tree.fb
            return mdclassify( observation, branch )

if __name__ == '__main__':
#     loadLocalData()
#     loadCarData()
    loadIrisData()
    tree = buildtree( my_data )
    drawtree( tree, jpeg = 'treeview.jpg' )
#     print classify(['vhigh', 'vhigh', '2', '3', 'small', 'low'], tree)
    print classify( [5.5, 2.5, 4.0, 1.3], tree )
    print classify( [6.7, 3.0, 5.2, 2.3], tree )
    prune( tree, 0.3 )
    # 即使是没有任何值，也要赋值为None
    drawtree( tree, jpeg = 'mdTreeView.jpg' )
#     print mdclassify(['vhigh', 'vhigh', '2', '3', 'small', 'low'],tree)

