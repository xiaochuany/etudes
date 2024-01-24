# %%
class MountainArr:
    def __init__(self,lst): self.lst = lst
    def get(self,k): return self.lst[k]
    def length(self): return len(self.lst)

# %%
def find(target,mountain_arr):
    n = mountain_arr.length()
    lo,hi = 0,n-1
    # find peak
    p=-1
    while lo<hi-1:
        mid = (lo+hi)//2
        x,y,z = mountain_arr.get(mid-1), mountain_arr.get(mid),mountain_arr.get(mid+1)
        if x<y and y>z: p=mid; break
        elif x<y<z: lo=mid
        else: hi=mid
    # parse left: increasing seq
    lo,hi=0,p
    while lo<hi:
        mid= (lo+hi)//2
        val = mountain_arr.get(mid)
        if val==target: return mid
        elif val<target: lo=mid+1
        else: hi=mid-1
    res0=lo if mountain_arr.get(lo)==target else -1
    if res0>-1: return res0 
    # parse right: decreasing seq
    lo,hi=p,n-1
    while lo<hi:
        mid = (lo+hi)//2
        val = mountain_arr.get(mid)
        if val==target: return mid
        elif val<target: hi=mid-1
        else: lo=mid+1
    res1=lo if mountain_arr.get(lo)==target else -1
    return lo if res1>-1 else -1

# %%
def test_find():
    mountain_arr = MountainArr([1,2,3,2,1,0])
    assert find(100,mountain_arr)==-1
    assert find(3,mountain_arr)==2

# %%



