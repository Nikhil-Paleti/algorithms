# topics: dp

from functools import lru_cache
from typing import List 

class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        m = len(matrix)
        n = len(matrix[0])

        @lru_cache(None)
        def dp(i, j):
            if i == m or j == n:
                return 0
            
            if i < 0 or j < 0:
                return 0
            
            if matrix[i][j] == "0":
                return 0
            
            neighbours = [dp(i-1, j-1), dp(i, j-1), dp(i-1, j)]
            return min(neighbours) + 1
        
        area = 0
        for i in range(m):
            for j in range(n):
                area = max(area, dp(i, j)**2)

        return area
        