from typing import List

def sum_sar_min(arr: List[int]) -> int:
        """sum over min of subarrays: stack+dp"""

        def prev_smaller(lst):
            """find index of previous smaller element, -1 if it does not exist"""
            stack=[]
            res = [None]*len(lst)
            for i,v in enumerate(lst):
                if not stack: res[i]=-1
                else:
                    while stack and stack[-1][0]>=v: stack.pop()
                    res[i]=stack[-1][1] if stack else -1
                stack.append([v,i])
            return res

        dp = [None]*len(arr)
        psi = prev_smaller(arr)
        for i,a in enumerate(arr):
            if psi[i]==-1: dp[i]= (i+1)*a
            else: dp[i] = dp[psi[i]]+ (i-psi[i])*a
        return sum(dp) % (10**9+7)


def test_sum_sar_min():
     assert sum_sar_min([3,1,2,4])==17
     assert sum_sar_min([1,2])==4