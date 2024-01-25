#2024-01-25
from typing import List

def find_peak(nums: List[int]) -> int:
        n = len(nums)
        if n==1: return 0
        if n==2: return 1 if nums[1]>nums[0] else 0
        lo, hi = 0, n-1
        while lo<hi-1:
            mid = (lo+hi)//2
            x,y,z= nums[mid-1],nums[mid],nums[mid+1]
            if x<y and y>z: return mid
            elif x<=y<=z: lo = mid
            else: hi=mid
        return lo if nums[lo]>nums[hi] else hi

def test_find_peak():
    assert find_peak([1,2,1,3,1]) in (1,4)
    assert find_peak([1,2,3])==2