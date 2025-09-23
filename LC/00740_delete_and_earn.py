# topics: dp

"""
state: i, max points till index i of freq
dp[i] = max(dp[i-1], dp[i-2]+points[i])
"""

from typing import List 

def deleteAndEarn(self, nums: List[int]) -> int:
    frequencies = {}
    max_number = float('-inf')
    for n in nums:
        max_number = max(max_number, n)
        if n in frequencies:
            frequencies[n] += 1
        else:
            frequencies[n] = 1
    
    points = [0] * (max_number +1 )
    for k,v in frequencies.items():
        points[k] = v*k

    two_back = points[0]
    one_back = points[1]
    for i in range(2, max_number+1):
        curr = max(one_back, two_back + points[i])
        two_back = one_back
        one_back = curr
    
    return curr