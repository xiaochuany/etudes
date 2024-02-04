#03-103.py

from typing import Optional, List

class TreeNode:
    def __init__(self,val=0,left=None,right=None) -> None:
        self.val=val
        self.left=left
        self.right=right


def zigzag_lev_order(root: Optional[TreeNode]) -> List[List[int]]:
        if not root: return []
        i = 1
        frontier={root}
        res=[[root.val]]
        while frontier:
            nxt = []
            vls = []
            for u in frontier:
                for v in [u.left,u.right]:
                    if v:
                        nxt.append(v)
                        vls.append(v.val)
            vls = vls[::-1] if i%2 else vls
            if vls: res.append(vls) 
            frontier=nxt
            i+=1
        return res

def test_zigzag_lev_order():
    node = TreeNode(0)
    node.left = TreeNode(1)
    node.right= TreeNode(2)
    node.left.left = TreeNode(3)
    node.left.right = TreeNode(4)
    node.right.right=TreeNode(6)
    assert zigzag_lev_order(node)== [[0],[2,1],[3,4,6]]