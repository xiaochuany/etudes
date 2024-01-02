#2024-01-02-2610

from itertools import zip_longest
from collections import Counter
from typing import List

def find_matrix(nums:List[int])-> List[List[int]]:
    c = [[k]*v for k,v in Counter(nums).items()]
    res = []
    for row in zip_longest(*c):
        res.append([v for v in row if v is not None])
    return res


class TestFindMatrix:
    nums0 = [2,3,6,2]
    x0 = find_matrix(nums0)
    nums1 = [9,9,9]
    x1 = find_matrix(nums1)

    def test_len(self):
        for x,n in zip([self.x0,self.x1],[self.nums0,self.nums1]):
            assert sum(map(len,x)) == len(n)

    def test_distinct(self):
        for x in [self.x0,self.x1]:
            assert all([len(set(row))==len(row) for row in x])