#2024-01-17-1207
from collections import Counter
from typing import List

def unique_occ(arr: List[int])->bool:
    cnt = Counter(arr)
    occ = Counter(cnt.values())
    return all([v==1 for v in occ.values()])

def test_unique_occ():
    assert unique_occ([1,2])==False
    assert unique_occ([1,1,1,2,2,3])==True
