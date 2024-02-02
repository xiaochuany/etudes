#2024-01-31-1891.py
from typing import List

def max_len(ribbons: List[int], k: int) -> int:
    def possible_at(length,ribbons,k):
        return sum([r//length for r in ribbons])>=k
    lo,hi=1,max(ribbons)+1
    while lo<hi:
        mid = (lo+hi)//2
        if possible_at(mid,ribbons,k): lo=mid+1
        else: hi=mid
    return lo-1

def test_max_len():
    assert max_len([2,3,4],4)==2
    assert max_len([2,3],5)==1
    assert max_len([4],5)==0

