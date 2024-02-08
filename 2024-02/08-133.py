#08-133.py

from typing import Optional
from collections import defaultdict

class Node:
     def __init__(self,val, neighbors=None) -> None:
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def clone_graph(node: Optional['Node']) -> Optional['Node']:
        if not node: return 
        clone = defaultdict(list)
        clone[node.val]=[n.val for n in node.neighbors]
        seen = {node}
        frontier = {node}
        while frontier:
            nxt = []
            for u in frontier:
                for v in u.neighbors:
                    if  v not in seen:
                        seen.add(v)
                        nxt.append(v)
                        clone[v.val].extend([n.val for n in v.neighbors])
            frontier=nxt
        v2n = {v:Node(v) for v in clone}
        for k,vs in clone.items():
            v2n[k].neighbors=[v2n[v] for v in vs]
        return v2n[node.val]

V = {i:Node(i) for i in range(4)}
for i in range(4):
     V[i].neighbors.append(V[(i+1)%4])

def test_clone_graph():
    assert id(clone_graph(V[3])) != id(V[3])
    assert clone_graph(V[3]).val == 3