#2024-01-26-540.py

from typing import List

def single_non_dup(nums: List[int]) -> int:
    lo,hi=0,len(nums)-1
    while lo<hi:
        mid=(lo+hi)//2
        if (mid%2==0 and nums[mid]==nums[mid+1]) or (mid%2==1 and nums[mid]==nums[mid-1]):
            lo=mid+1
        else: hi=mid
    return nums[lo]

def test_single_non_dup():
    assert single_non_dup([1,1,2,2,3])==3, 'incorrect annswer!'
