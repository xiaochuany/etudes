from typing import List

def min_fall(matrix: List[List[int]]) -> int:
    """minimise sum of falling paths"""
    dp = [matrix[0].copy() for _ in range(len(matrix))]
    for i,row in enumerate(matrix):
        if i==0: continue
        for j,val in enumerate(row):
            if j==0:  
                dp[i][j]= val+ min(dp[i-1][j], dp[i-1][j+1])
            if 0<j<len(row)-1:
                dp[i][j]= val+ min(dp[i-1][j], dp[i-1][j-1], dp[i-1][j+1])
            if j==len(row)-1:
                dp[i][j]= val+ min(dp[i-1][j], dp[i-1][j-1])
    return min(dp[-1])


def test_min_fall():
    assert min_fall([[-19,57],[-40,-5]])==-59