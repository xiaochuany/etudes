#2023-12-30-1897
from itertools import chain
from collections import Counter
from typing import List

def make_equal(words:List[str])->bool:
    """make a list of words equal, arbitrary number of operations allowed"""
    return all(v%len(words)==0 for v in Counter(chain(*words)).values())

class TestMakeEqual:
    def test(self):
        assert make_equal(['abb','bba','bab']) is True
        assert make_equal(['ab','a']) is False
        assert make_equal(['aabb','aa']) is True
