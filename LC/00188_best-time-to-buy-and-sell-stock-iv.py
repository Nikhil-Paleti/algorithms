# topics: dp

from functools import lru_cache

class Solution:
    def maxProfit(self, k: int, prices: list[int]) -> int:
        @lru_cache(None)
        def dp(day, transactions_left, holding):
            if day == len(prices):
                return 0

            if transactions_left == 0:
                return 0

            # do nothing 
            do_nothing = dp(day+1, transactions_left, holding)

            if holding:
                # we can sell
                profit = prices[day] + dp(day+1, transactions_left-1, 0)
            else:
                # we can buy
                profit = -prices[day] + dp(day+1, transactions_left, 1)
            
            return max(do_nothing, profit)

        return dp(0, k, 0)