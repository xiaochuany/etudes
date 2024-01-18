#2024-01-18-70
def climb_stair(n:int)->int:
    """every stride either 1 step or 2 steps, compute the number of ways of arriving at n starting from 0"""
    prev, curr = 1, 2
    for _ in range(n-2):
        prev, curr = curr, prev+curr
    return curr if n>1 else prev

# %%
def test():
    assert climb_stair(4)==5

# %%



