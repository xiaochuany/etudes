# from fasthtml.common import *
import numpy as np
from collections import deque

# app, rt = fast_app(live=True)
size = 9

def queens():
    while True:
        perm = np.random.permutation(size)
        if all(abs(perm[i] - perm[i + 1]) > 1 for i in range(size - 1)):
            break
    return perm

perm = queens()


def coloring():
    grid = np.full((size, size), -1)
    grid[np.arange(size), perm] = np.arange(size)
    queue = deque((i,n,i) for i,n in enumerate(perm))
    while queue:
        r, c, idx = queue.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size and grid[nr,nc] == -1:
                grid[nr,nc] = idx
                queue.append((nr,nc,idx))
    return grid