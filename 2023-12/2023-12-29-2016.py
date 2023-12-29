#2023-12-29-2016
import itertools
from typing import List

def max_diff(nums: List[int])-> int:
    """compute maximum difference of nums[j]-nums[i] with i<j and nums[i]<nums[j]"""
    res = -1
    for a,b in zip(itertools.accumulate(nums,min),nums):
        if b-a>0: res = max(res, b-a)
    return res

class TestMaxDiff:
    def test(self):
        assert max_diff([7,6,5,1])==-1
        assert max_diff([5,6,7,8])==3
        assert max_diff([6,6,6])==-1