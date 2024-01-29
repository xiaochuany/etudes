import itertools, random
from bisect import bisect_left
from typing import List

def sample_idx(w:List[int])->int:
    s=sum(w)
    p =list(itertools.accumulate(w))
    return bisect_left(p,random.uniform(0,1)*s)


def test_sample_idx():
    assert sample_idx([0,1])==1
    assert sample_idx([1,0])==0
    N=100000
    f = sum([sample_idx([2,1]) for _ in range(N)])/N
    assert 0.32<f<0.34, "vialating LLN!"
