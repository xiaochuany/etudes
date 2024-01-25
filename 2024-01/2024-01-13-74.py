#2024-01-13-74
from typing import List

def search_matrix(matrix: List[List[int]], target: int) -> bool:
        m, n =len(matrix), len(matrix[0])
        lo,hi=0,m-1
        while lo<hi-1:
            mid=(lo+hi)//2
            if matrix[mid][0]==target: return 1
            if matrix[mid][0]>target: hi=mid-1
            if matrix[mid][0]<target: lo=mid
        row = matrix[lo] if target<matrix[hi][0] else matrix[hi]
        lo,hi=0,n-1
        while lo<hi:
            mid=(lo+hi)//2
            if row[mid]==target: return 1
            if row[mid]>target: hi=mid-1
            if row[mid]<target: lo=mid+1
        return 1 if row[lo]==target else 0

def test_search_matrix():
     assert bool(search_matrix(matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13)) is False
     assert bool(search_matrix(matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 30)) is True