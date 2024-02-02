#02-1062.py

def repeat_at(k:int,s:str)->bool:
    """repeat_at is a monotone function of k (true then false) """
    word = s[:k]
    seen = set()
    for i in range(len(s)-k+1):
        h = hash(word)
        if h in seen: return True
        seen.add(h)
        if i<len(s)-k:
            word= word[1:]+s[i+k]
    return False

def longest_repeat_word(s:str)->int:
    """length of longest repeated substring
    binary search the idx of changing from true to false    
    """
    lo,hi=1,len(s)
    while lo<hi:
        mid = (lo+hi)//2
        if repeat_at(mid,s): lo=mid+1
        else: hi=mid
    return lo-1

def test_longest_repeat_word():
    s = 'ababa'
    k = 3
    assert repeat_at(k,s) is True
    assert longest_repeat_word('ababa')==3
    assert longest_repeat_word('abcd')==0