# topics: dp
"""
state: i, the current step
dp[i]: the minimum cost to reach step i
"""

from typing import List

def minCostClimbingStairs(cost: List[int]) -> int:
    n = len(cost)
    one_back = cost[0]
    two_back = cost[1]
    for i in range(2, n):
        current = cost[i] + min(one_back, two_back)
        one_back, two_back = two_back, current
    return min(one_back, two_back)