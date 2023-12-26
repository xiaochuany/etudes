import numpy as np

def dice_target(n:int, k:int, target:int):
    """
    fix k varying n and target, recurse
        f(t,m) = f(t-1,m-1)+...+f(t-k,m-1) 
    where f(non-positive, *) = 0
    """
    f = [[0]*(n+1) for _ in range(target+1)]
    for i in range(1,k+1):
        if i<=target: f[i][1]=1
    for m in range(2,n+1):
        for t in range(target+1):
            f[t][m]= sum([f[t-i][m-1] for i in range(1,k+1) if t-i>=0])
    return f[target][n]%(1000000000+7)

def dice_target_np(n:int, k:int, target:int):
    f = np.zeros((target+1,n+1),dtype=np.int64)
    f[1:k+1,1]=1
    A = np.tril(np.ones((target+1,target+1)),-1) - np.tril(np.ones((target+1,target+1)),-(k+1))
    for m in range(2,n+1):
        f[:,m]=  A@f[:,m-1]     
    return f[target,n]%(1000000000+7)

class TestDice:
    def test_py(self):
        assert dice_target(2,6,7)==6
        assert dice_target(15,15,160)==885652316
    def test_np(self):
        assert dice_target_np(15,15,180)==dice_target(15,15,180)
        