# topics: dp

"""
state: i, the current house
dp[i]: the maximum amount of money we can rob from the first i houses
"""

from typing import List 

def rob(nums: List[int]) -> int:
    n = len(nums)
    if n == 1:
        return nums[0]
    two_back = nums[0]
    one_back = max(nums[0], nums[1])
    for i in range(2, n):
        current = max(one_back, two_back + nums[i])
        two_back = one_back
        one_back = current

    return one_back