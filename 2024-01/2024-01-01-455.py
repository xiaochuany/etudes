#2024-01-01-455
from typing import List

def match_gt(g: List[int], s: List[int]) -> int:
    """ match si with gj as many as possible. Condition: si>=gj"""
    g.sort(reverse=True);s.sort(reverse=True)
    res=j=0
    for i,si in enumerate(s):
        while j<len(g):
            if si>=g[j]: res+=1; j+=1; break
            j+=1
        if j==len(g): break
    return res

class TestMatchGt:
  def test(self):
    assert match_gt([2,4,1], [1,1,1])==1
    assert match_gt