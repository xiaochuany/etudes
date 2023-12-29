def makealternate(s:str)->int:
    cnt = 0
    for i,ch in enumerate(s):
        if ch!=str(i%2): cnt+=1
    return cnt if cnt<=len(s)//2 else len(s)-cnt

def test():
    assert makealternate('010101')==0
    assert makealternate('1111')==2
    

