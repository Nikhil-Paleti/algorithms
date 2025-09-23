# topics: dp
"""
state: i,m which say i numbers used and m multiples used.
dp[i,m]: max score by starting from i and m
"""

from functools import lru_cache
from typing import List

def maximumScore(self, nums: List[int], multipliers: List[int]) -> int:
    n = len(nums)
    m = len(multipliers)

    @lru_cache(None)
    def dp(i, j):
        if j == m:
            return 0
        
        right = (n-1) - (j-i)
        picking_left = nums[i] * multipliers[j] + dp(i+1, j+1)
        picking_right = nums[right] * multipliers[j] + dp(i, j+1)

        return max(picking_left, picking_right)
            
    return dp(0, 0)