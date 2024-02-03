#04-102.py

from typing import Optional,List

class TreeNode:
    def __init__(self,val=0,left=None,right=None) -> None:
        self.val=val
        self.left=left
        self.right=right

def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    if not root: return []
    res = [[root.val]]
    seen={root}
    frontier={root}
    while frontier:
        next_=[]
        vals=[]
        for u in frontier:
            for v in [u.left, u.right]:
                if v and v not in seen:
                    seen.add(v)
                    next_.append(v)
                    vals.append(v.val)
        frontier=next_
        if frontier:
            res.append(vals)
    return res

def test_level_order():
    node = TreeNode(0)
    node.left = TreeNode(1)
    node.right= TreeNode(2)
    node.left.left = TreeNode(3)
    node.left.right = TreeNode(4)
    node.right.right=TreeNode(6)
    assert level_order(node) == [[0],[1,2],[3,4,6]]