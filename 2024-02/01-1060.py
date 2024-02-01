#01-1060.py

from typing import List

def miel(nums: List[int], k: int) -> int:
    """given positive increasing nums, find kth element NOT in nums starting from nums[0]

    a tiny adjustment of bisect_left 
    """
    lo,hi = 0,len(nums)
    while lo<hi:
        mid=(lo+hi)//2
        if nums[mid]-nums[0]-mid < k: lo=mid+1
        else: hi=mid
    idx=lo-1 # necessarily idx>=0 because the sequence nums[i]-nums[0]-i is 0 at i=0
    return nums[idx]+(k - nums[idx]+nums[0]+idx)


def test_miel():
    assert miel([4,7,9,10],1)==5
    assert miel([4,7,9,10],3)==8
    assert miel([1,2,3],3)==6