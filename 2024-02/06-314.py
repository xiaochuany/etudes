#06-314.py

from typing import Optional, List
from collections import defaultdict

class TreeNode:
    def __init__(self,val=0,left=None,right=None) -> None:
        self.val=val
        self.left=left
        self.right=right

def vertical_order(root: Optional[TreeNode]) -> List[List[int]]:
    if not root: return []
    col={root:0}
    frontier=[root]
    while frontier:
        nxt = []
        for u in frontier:
            if u.left:
                col[u.left]=col[u]-1
                nxt.append(u.left)
            if u.right:
                col[u.right]=col[u]+1
                nxt.append(u.right)
        frontier = nxt
    res = defaultdict(list)
    for k,v in col.items():
        res[v].append(k.val)
    res_sort = sorted([(k,v) for k,v in res.items()],key=lambda o:o[0])
    return [y for _,y in res_sort]

def test_vert_order():
    node = TreeNode(0)
    node.left = TreeNode(1)
    node.right= TreeNode(2)
    node.left.left = TreeNode(3)
    node.left.right = TreeNode(4)
    node.right.right=TreeNode(6)
    assert vertical_order(node) == [[3],[1],[0,4],[2],[6]]