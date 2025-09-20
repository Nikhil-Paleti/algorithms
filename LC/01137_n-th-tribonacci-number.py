# topics: dp
"""
State: i, the ith number
dp[i] = dp[i-1] + dp[i-2] + dp[i-3]
"""

def tribonacci(self, n: int) -> int:
    if n < 1:
        return 0
    if n <= 2:
        return 1
    
    t_1 = 0
    t_2 = 1
    t_3 = 1

    for i in range(3, n+1):
        current = t_1 + t_2 + t_3
        t_1 = t_2
        t_2 = t_3 
        t_3 = current
    
    return current

