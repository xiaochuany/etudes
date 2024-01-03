# %%
from typing import List

# %%
def number_beams(bank: List[str]) -> int:
    """two laser devices make beam iff i) not same row ii) no devices at all in any row in between"""
    rs = []
    for row in bank:
        if (a:=row.count('1')): rs.append(a)
    return sum([pre*nex for pre, nex in zip(rs,rs[1:])])

# %%
def test_number_beams():
    assert number_beams(['001','111', '000', '1111'])==15
    assert number_beams(['000','0111','00'])==0