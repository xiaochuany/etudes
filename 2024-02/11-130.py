#11-130.py

from typing import List

def solve(board:List[List[str]])->None:
    m,n=len(board),len(board[0])
    seen=set()
    for i in range(m):
        for j in range(n):
            if board[i][j]=='O' and (i,j) not in seen:
                frontier=[(i,j)]
                cluster=[(i,j)]
                boundary = True if i==0 or i==m-1 or j==0 or j==n-1 else False
                while frontier:
                    nxt=[]
                    for x,y in frontier:
                        for d1,d2 in [(0,1),(0,-1),(1,0),(-1,0)]:
                            if 0<=x+d1<m and 0<=y+d2<n and board[x+d1][y+d2]=='O' and (x+d1,y+d2) not in seen:
                                seen.add((x+d1,y+d2))
                                nxt.append((x+d1,y+d2))
                                cluster.append((x+d1,y+d2))
                                if x+d1==0 or x+d1==m-1 or y+d2==0 or y+d2==n-1: boundary=True
                    frontier=nxt
                if not boundary:
                    for z1,z2 in cluster: board[z1][z2]='X'
    return 

def test_solve():
    board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]
    solve(board)
    assert board == [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]