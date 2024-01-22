#2024-01-22-645

from typing import List

def find_error(nums:List[int])->List[int]:
    res = []
    org = set(range(1,len(nums)+1))
    for n in nums:
        if n in org: org.remove(n)
        else: res.append(n)
    res.append(org.pop())
    return res

def test_find_error():
    assert sorted(find_error([1,2,4,2]))==[2,3]