from collections import Counter

def isPathCrossing(path:str)->str:
    pos = [(0,0)]
    dirs = {'N': (0,1), 'S':(0,-1), 'E': (1,0), 'W':(-1,0)}
    for i,c in enumerate(path):
        x,y = dirs[c]
        pos.append((pos[-1][0]+x, pos[-1][1]+y))
    C = Counter(pos)
    return max(C.values())>1

def test():
    assert isPathCrossing('NS')==True

test()
