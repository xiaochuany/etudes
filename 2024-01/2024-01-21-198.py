from typing import List

def rob(nums:List[int])->int:
    """max sum over all subsequences having no consecutive elements. 
    assumption: num in nums are all non-negative"""
    if len(nums)<=2: return max(nums)

    dp = [None]*len(nums)
    
    if (a:=nums[0]+nums[2])>nums[1]: 
        dp[:3]= [nums[0],max(nums[:2]),a]
    else: 
        dp[:3]=[*nums[:2], nums[1]]
    
    for i in range(3,len(nums)):
        keep = dp[i-2]+nums[i]
        drop = dp[i-3]+nums[i-1]
        dp[i]=max(keep,drop)
    return max(dp)


def test_rob():
    assert rob([1,2,3,1])==4
    assert rob([2,7,9,3,1])==12