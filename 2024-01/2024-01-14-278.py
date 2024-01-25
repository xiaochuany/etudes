#2024-01-14-278

class Version:
    def __init__(self,lst): 
        self.lst=[None]+lst # version starts from 1
        self.n=len(lst)
    def isBad(self,k): return self.lst[k]

def check_bad(ver:Version)->int:
    """n is the total number of versions, a version is bad then all version after are bad
    find the first bad version"""
    lo,hi=1,ver.n
    while lo<hi:
        mid=(lo+hi)//2
        if ver.isBad(mid): hi=mid
        else: lo=mid+1
    return lo

def test_bad():
    ver = Version([False]*2+[True]*8)
    assert check_bad(ver)==3