#10-323.py
from typing import List
from collections import defaultdict

def count_components(n: int, edges: List[List[int]]) -> int:
        # build graph
        graph = defaultdict(list)
        for a,b in edges:
            graph[a].append(b)
            graph[b].append(a)
        # initialisation
        comp = 0
        seen = set()
        # loop through all nodes, increment comp by 1 if see new node (new cluster)
        for i in range(n):
            if i not in seen: 
                comp+=1
                seen.add(i)
                frontier=[i]
            else: frontier=[]
            # if frontier: visit all nodes connected to frontier, mark them as seen 
            while frontier:
                nxt=[]
                for u in frontier:
                    for v in graph[u]:
                        if v not in seen:
                            seen.add(v)
                            nxt.append(v)
                frontier=nxt
        return comp

def test_count_components():
     assert count_components(n = 5, edges = [[0,1],[1,2],[3,4]]) == 2