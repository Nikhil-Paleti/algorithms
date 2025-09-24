# topics: dp

from functools import lru_cache 

class Solution:
    def change(self, amount: int, coins: list[int]) -> int:
        
        @lru_cache(None)
        def dp(pending_amount, i):
            if pending_amount == 0:
                return 1
            if pending_amount < 0 or i == len(coins):
                return 0
            
            count = 0
            count += dp(pending_amount - coins[i], i)        
            count += dp(pending_amount, i+1)
            
            return count
        
        return dp(amount,  0)