# %%
# 2024-01-16-2225
from collections import Counter
from typing import List

# %%
def find_winners(matches: List[List[int]]) -> List[List[int]]:
    """find always-winners, find one-time-loser"""
    winners = Counter([match[0] for match in matches])
    losers = Counter([match[1] for match in matches])
    # in winners but not in losers:
    a0 = winners.keys() - losers.keys()
    a0 = sorted(list(a0))
    # loser count = 1
    a1 = sorted([k for k,v in losers.items() if v==1])
    return [a0,a1]

# %%
def test_find_winners():
    assert find_winners([[1,3],[2,3],[3,6],[5,6],[5,7],[4,5],[4,8],[4,9],[10,4],[10,9]])==[[1,2,10],[4,5,7,8]]
    assert find_winners([[2,3],[1,3],[5,4],[6,4]]) == [[1,2,5,6],[]]

# %%



