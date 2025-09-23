# topics: dp

from functools import lru_cache

class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        if amount == 0:
            return 0

        # keep only useful denominations
        coins = [c for c in coins if c <= amount]
        if not coins:
            return -1

        @lru_cache(None)
        def dp(pending_amount: int) -> int:
            if pending_amount == 0:
                return 0

            best = float('inf')
            for current_denomination in coins:
                if pending_amount >= current_denomination:
                    sub = dp(pending_amount - current_denomination)
                    if sub != float('inf'):
                        best = min(best, 1 + sub)
            return best

        ans = dp(amount)
        return -1 if ans == float('inf') else ans