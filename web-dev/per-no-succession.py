"""queens position in a table, click to remove/add (flip 0/1) queens"""

from fasthtml.common import *
import numpy as np

app,rt = fast_app(live=True)
size=6

def queens():
    while True:
        perm = np.random.permutation(size)
        if all(abs(perm[i]-perm[i+1])>1 for i in range(size-1)): break
    return np.eye(size,dtype=int)[perm]

def tdx(e):
    return Td(e, hx_post=f"/flip/{e}", hx_swap="outerHTML")

@rt("/")
def get():
    arr_td = [map(tdx, row) for row in queens()]
    return Table(*map(Tr,arr_td))

@rt("/flip/{e}")
def post(e:int):
    return tdx(1-e)

serve()