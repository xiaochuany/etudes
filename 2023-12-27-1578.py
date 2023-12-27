# 1578 min cost to make rope colorful
from typing import List

def min_cost(colors:str, costs:List[int])->int:
    """same length, deduplite colors in a way that minimize cost
    one pass: check whether the current color is the same as before
     - if yes, accumulate cost and compute running maximum
     - if not, s-m represent the cost of deduplication, reset s=m=0
    """
    s = m = cost = 0
    for i,c in enumerate(colors):
        previous = None if i==0 else colors[i-1]
        if c!=previous: 
            cost+= (s-m); s=m=0
        s += costs[i]
        m = max(m, costs[i])
    return cost + s-m   # cost of final set of duplicates is stored in s-m
    
class TestMinCost:
    def test_mc(self):
        assert min_cost('aabaa',[1,2,3,4,1])==2