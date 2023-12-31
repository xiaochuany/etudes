from collections import defaultdict

def max_word(s: str) -> int:
    """compute the longest word length between equal characters, return -1 if non existing"""
    res = -1
    dd = defaultdict(list)
    for i,c in enumerate(s):
        dd[c].append(i)
    for v in dd.values():
        max_diff = max(v)-min(v)-1
        res = max(res, max_diff)
    return res

class TestMaxWord:
    def test(self):
        assert max_word('abbbba')==4
        assert max_word('a') == -1
        assert max_word('abcdefg')==-1
        assert max_word('aaaa')==2



