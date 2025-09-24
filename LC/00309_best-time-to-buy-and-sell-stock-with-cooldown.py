# topics: dp

from functools import lru_cache

class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        
        @lru_cache(None)
        def dp(day, holding):
            if day >= len(prices):
                return 0

            # do nothing 
            do_nothing = dp(day+1, holding)

            if holding:
                # we are selling
                do_something = prices[day] + dp(day + 2, 0)
            else:
                do_something = -prices[day] + dp(day+1, 1)
            
            return max(do_nothing, do_something)
        
        return dp(0, 0)
        