#09-490.py

from typing import List

def has_path(maze: List[List[int]], start: List[int], destination: List[int]) -> bool:
        m,n = len(maze),len(maze[0])
        maze_pad = [[1]*(n+2)] + [[1]+row+[1] for row in maze] + [[1]*(n+2)]
        up = (0,1)
        down=(0,-1)
        left = (1,0)
        right= (-1,0)
        seen = {(start[0]+1,start[1]+1)}
        frontier = [(start[0]+1,start[1]+1)]
        while frontier:
            nxt = []
            for x,y in frontier:
                for d1,d2 in [up,down,left,right]:
                    c1,c2=x,y
                    while maze_pad[c1+d1][c2+d2]==0:
                        c1+=d1; c2+=d2
                    if (c1,c2) not in seen:
                        seen.add((c1,c2))
                        nxt.append((c1,c2))
            frontier=nxt
        z1,z2 = destination
        return (z1+1,z2+1) in seen

def test_has_path():
    maze = [[0,0,1,0,0],[0,0,0,0,0],[0,0,0,1,0],[1,1,0,1,1],[0,0,0,0,0]]
    assert has_path(maze, start = [0,4], destination = [4,4]) is True
    assert has_path(maze, start = [0,4], destination = [3,2]) is False