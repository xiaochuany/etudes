#12-207.py

from collections import defaultdict
from typing import List

def can_finish(num: int, prerequisites: List[List[int]]) -> bool:
    """cycle detection"""
    # build the graph
    gr = defaultdict(list)
    for a,b in prerequisites: 
        gr[b].append(a)
        if a==b: return False # trivial cycle
    # define dfs: visit all nodes reachable from s 
    # record finishing order in finished.
    def dfs(gr,s):
        for v in gr[s]:
            if v not in seen:
                seen.add(v)
                dfs(gr,v)
                finished.append(v)
    seen=set()
    finished=[]
    for i in range(num):
        if i not in seen:
            seen.add(i)
            dfs(gr,i)
            finished.append(i)
    # record reversed finishing order in a hashmap 
    fmap = {el:i for i,el in enumerate(reversed(finished))}
    for k,lst in gr.items():
        for v in lst:
            if fmap[k]>fmap[v]: return False
    return True

def test_can_finish():
    prerequisites = [[0,10],[3,18],[6,11],[11,14],[13,1],[15,1],[17,4]]
    assert can_finish(10,[[5,5]]) is False
    assert can_finish(20,prerequisites) is True
