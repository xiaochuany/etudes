#
from typing import Tuple, List
from collections import defaultdict

# %%
class Stream:
    def __init__(self, data:List[str]=[]):
        self.d = defaultdict(int)
        self.s = set()
        self.curr_max = 0
        for item in data: self.add(item)
        
    def add(self,item:str):
        self.d[item]+=1
        if self.d[item]>self.curr_max: 
            self.s.clear(); self.s.add(item); self.curr_max=self.d[item]
        elif self.d[item]==self.curr_max: self.s.add(item)

    @property
    def most_liked(self):
        return self.s

# %%
def test():
    stream=Stream(list('aabbcc'))
    assert stream.most_liked == set('abc')
    stream.add('d')
    stream.add('a')
    assert stream.most_liked == set('a')

# %%



