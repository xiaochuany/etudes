#07-200.py
from typing import List

def compt_count(grid: List[List[str]]) -> int:
        m = len(grid)
        n = len(grid[0])
        dirs = [(-1,0),(1,0),(0,1),(0,-1)]
        grid_pad = [['0']*(n+2)]+[['0']+row+['0'] for row in grid] + [['0']*(n+2)]
        graph = {(i,j): [(i+k,j+l) for (k,l) in dirs if grid_pad[i+k][j+l]=='1'] for i in range(1,m+1) for j in range(1,n+1) if grid_pad[i][j]=='1'}
        n_compt=0
        visited=set()
        for node in graph:
            if node not in visited:
                n_compt+=1
                frontier=[node]
                while frontier:
                    nxt = []
                    for u in frontier:
                        for v in graph[u]:
                            if v not in visited:
                                visited.add(v)
                                nxt.append(v)
                    frontier=nxt
        return n_compt

def test_compt_count():
     assert compt_count([["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]])==3 