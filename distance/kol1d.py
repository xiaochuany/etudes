import numpy as np

def _get_diff(x,y):
    assert x.size == y.size
    assert x.ndim == y.ndim == 1
    x = np.sort(x)
    x = x[:,None]
    y = y[None,:]
    res = np.sum(y<x, axis=1, keepdims=False) - np.arange(x.size)
    return res.max()/x.size

def kol1d(x,y): 
    return max(_get_diff(x,y), _get_diff(y,x))

if __name__ == "__main__":
    x, y = np.random.default_rng(0).standard_t(df=2.,size=(2,10000))
    res  = kol1d(x,y)
    print(f"{res.item()=} should be small!")
