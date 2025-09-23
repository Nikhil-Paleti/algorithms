# topics: dp

from functools import lru_cache

class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:

        @lru_cache(None)
        def dp(i: int) -> bool:
            if i == len(s):
                return True
            
            for w in wordDict:
                if len(s) - i >= len(w) and s[i : i + len(w)] == w:
                    if dp(i + len(w)):
                        return True
            
            return False

        return dp(0)