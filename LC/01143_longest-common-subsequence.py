# topics: dp
"""
state: i,j the index i and j from text1 and text2
dp[i,j] = the max common starting from index i,j
"""

from functools import lru_cache

def longestCommonSubsequence(self, text1: str, text2: str) -> int:
    m = len(text1)
    n = len(text2)

    @lru_cache(None)
    def dp(i, j):
        if i == m or j == n:
            return 0
        
        if text1[i] == text2[j]:
            return 1 + dp(i+1, j+1)
        
        return max(dp(i+1, j), dp(i, j+1))
    
    return dp(0,0)