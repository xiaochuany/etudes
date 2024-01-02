#2024-01-02-1481
from collections import Counter

def f(nums,k):
    """min distinct chars after removing k elem"""
    if k>= len(nums): return 0
    c = [v for v in Counter(nums).values()]
    c.sort(reverse=True)
    for _ in range(k):
        c[-1]-=1
        if c[-1]==0: c.pop()
    return len(c)

def test_f():
    assert f([3,3,3,4,4,5],3)==1
    assert f([3,3,3],4)== 0



