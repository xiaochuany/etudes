from typing import List

def search(nums:List[int], t)->int:
    """nums is obtained by rotating a sorted array with distinct elements, find idx of target t"""
    l, h = 0, len(nums)-1
    while l<h:
        m = (l+h)//2
        if nums[m]==t: return m
        else: 
            if nums[l]<=nums[m]: # left half is sorted
                if nums[l]<=t<nums[m]: h=m-1
                else: l=m+1
            else: # right half is sorted
                if nums[m]<t<=nums[h]: l=m+1
                else: h=m-1
    return h if nums[h]==t else -1


def test_search():
    assert search([1,2,3],3)==2
    assert search([5,1,3],3)==2
    assert search([5,1,3],4)==-1

