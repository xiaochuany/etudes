#2024-01-30-1300.py
from itertools import accumulate
from bisect import bisect_left
from typing import List

def find_best_val(arr: List[int], target: int) -> int:
        """find val such that  sum(min(a,val) for a in arr) is as close to target as possible"""
        arr.sort()
        n=len(arr)
        acc = list(accumulate(arr))
        ss = [s+(n-i-1)*v for i,(v,s) in enumerate(zip(arr,acc))]
        if ss[0]>target: 
            k,m = target//len(ss), target%len(ss)
            return k if m<= (k*len(ss)+len(ss)-target) else k+1
        elif ss[-1]<target: return arr[-1]
        else:
            i = bisect_left(ss,target)
            ## now try all values from arr[i-1] to arr[i] inclusive
            vs = [(v,acc[i-1]+(n-i)*v) for v in range(arr[i-1],arr[i]+1)]
            ib = bisect_left(vs, target, key=lambda o:o[1]) # ib>=1
            if vs[ib][1]+vs[ib-1][1]>=2*target: return vs[ib-1][0]
            else: return vs[ib][0]


def test_find_best_val():
     assert find_best_val([3,4,5], 12)==5
     assert find_best_val([5,4,3],12)==5
     assert find_best_val([10,10,10,10], 100)==10
     assert find_best_val([10,10,10,10],20)==5
    