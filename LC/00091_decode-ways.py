# topics: dp

from functools import lru_cache

class Solution:
    def numDecodings(self, s: str) -> int:

        @lru_cache(None)
        def dp(i: int) -> int:
            if i == len(s):
                return 1
            if s[i] == '0':          # cannot decode a leading zero
                return 0

            # take one character
            ways = dp(i + 1)

            # take two characters if valid (10..26)
            if i + 1 < len(s) and (s[i] == '1' or (s[i] == '2' and s[i + 1] <= '6')):
                ways += dp(i + 2)

            return ways

        return dp(0)