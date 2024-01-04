# %%
from collections import Counter
from typing import List

# %%
def min_ops(nums:List[int])->int:
    """admissible ops: either remove pair of identical int or triple of identical int"""
    res=0
    for v in Counter(nums).values():
        if v==1: res = -1; break
        k, r = v//3, v%3
        if not r: res+=k
        else: res+=(k+1)
    return res

# %%
def test_min_ops():
    assert min_ops([99]*1) == -1
    assert min_ops([99]*2) == 1
    assert min_ops([99]*100+[999]*30) == 44

# %%



