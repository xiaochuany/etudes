import string

def numDecodings(s: str) -> int:
        ctoi = {c:str(i+1) for i,c in enumerate(string.ascii_uppercase)}
        itoc = {i:c for c,i in ctoi.items()}        
        if len(s)<=1: return int(s in itoc)

        # init first two values
        dp = [0]*len(s)
        dp[0] = 1 if s[0] in itoc else 0
        
        if dp[0]==0: dp[1]=0
        elif s[:2] in itoc and s[1] in itoc: dp[1]=2
        elif s[:2] in itoc and s[1] not in itoc: dp[1]=1
        elif s[:2] not in itoc and s[1] in itoc: dp[1]=1
        else: dp[1]=0

        for i in range(2,len(s)):
            a, b = s[i-1:i+1]
            if b in itoc and a+b not in itoc: # 99
                dp[i] = dp[i-1]
            elif b not in itoc and a+b in itoc: # 10
                dp[i] = dp[i-2]
            elif b in itoc and a+b in itoc: # 31
                dp[i] = dp[i-1]+dp[i-2]
            else: dp[i]=0 # 50
        
        return dp[-1]

class TestNumsDecodings:
    def test_one(self):
        assert numDecodings('0')==0
        assert numDecodings('1')==1
    def test_more(self):
        assert numDecodings('226')==3
