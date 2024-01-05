from functools import reduce
from typing import List

def lis(nums:List[int])->int:
    """Claim: dp[i] is NOT necessarily the solution for sequence nums[:i], but max(dp) is the solution for nums.
    Proof: 
    (i) max(dp)>= len(sol)=:k. 
        Denote the indices of sol by (i1,...,ik). we have
        max(dp)>= dp[ik]>= dp[i(k-1)]+1 >= ... >=dp[i1]+1
        hence max(dp)>= dp[i1]+k-1 >= k
    (ii) max(dp)<= len(sol)=:k.
        suppose not. since we can increase by at most one the value of max(dp) for a fixed i in the loop, 
        there is at least k indices i1,...,ik, in each of these rounds of the for loop,
        max(dp) increases by 1. It must be the case that i0 (defined as any i with nums[i]<nums[i1]), i1,...,ik forms an incresasing sequence.
        contradicting len(sol)=k. 
    """
    dp = [1]*len(nums)
    for i in range(1,len(nums)):
        dp[i]=reduce(max,[dp[j]+1 for j in range(i) if nums[i]>nums[j]], dp[i])
    return max(dp)

def test_lis():
    assert lis([1,1,1])==1
    assert lis([1,2,4])==3
    assert lis([1,2,3,-9,-8,-7,-6])==4
    assert lis([7,6,5])==1
    assert lis([3])==1