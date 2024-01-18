#2024-01-15-1165
def srk(keyboard:str, word:str)->int:
    """time moving from letter i to j is |i-j| where i, j are pos on the keyboard. start pos=0"""
    hm = {ch:i for i,ch in enumerate(keyboard)}
    res = hm[word[0]]
    for ch1,ch2 in zip(word,word[1:]):
        res += abs(hm[ch1]-hm[ch2])
    return res

# %%
def test_srk():
    assert srk("abcdefghijklmnopqrstuvwxyz", 'cba')==4
