# import pandas as pd
from collections import namedtuple
from operator import itemgetter
from pprint import pformat
from scipy.spatial import distance
import math
class Node(namedtuple('Node','location left right')):
    def __repr__(self):
        return pformat(tuple(self))

def mk_kd_tree(pts,depth = 0):
    try:
        width = len(pts[0])
    except IndexError as e:
        return None

    axis = depth%width
    pts.sort(key = itemgetter(axis))

    median = len(pts)//2
    print(median)
    return Node(location = pts[median],left = mk_kd_tree(pts[:median],depth+1),right = mk_kd_tree(pts[median+1:],depth+1))

def dist(a,b):
    return distance.euclidean(a,b)

def search_kd_tree_k(tr,pt):
    pathes = []
    tmp_root = tr
    dp = 0
    width = len(pt)
    while tmp_root:
        axis = dp%width
        pathes.append((tmp_root,dp))
        if pt[axis] < tmp_root.location[axis] :
            tmp_root = tmp_root.left
        else:
            # print("asa")
            tmp_root = tmp_root.right
        dp = dp +1
    print(pathes)

    # search other road
    nearst = tr.location
    ndist = dist(pt,nearst)
    while len(pathes) > 0:
        path = pathes.pop()
        axis = path[1] % width
        if (dist(pt,path[0].location) < ndist):
            nearst = path[0].location
            ndist = dist(pt,path[0].location)       
        # search other tree
        if math.fabs(pt[axis] - path[0].location[axis]) < ndist:
            if (pt[axis] < path[0].location[axis] and path[0].right) :
                pathes.append(path[0].right)
            elif (pt[axis] > path[0].location[axis] and path[0].left):
                pathes.append(path[0].left)
    print(nearst)
    print(ndist)

if __name__ == '__main__':
    pts = [(2,3),(5,4),(9,6),(4,7),(8,1),(7,2)]
    tr = mk_kd_tree(pts)
    # print(tr)
    search_kd_tree_k(tr,(9,1))



