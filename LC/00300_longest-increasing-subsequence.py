# topics: dp

from functools import lru_cache

class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:

        @lru_cache(None)
        def dp(i):
            ans = 1

            for j in range(i-1, -1, -1):
                if nums[j] < nums[i]:
                    ans = max(dp(j) + 1, ans)
            
            return ans 
        
        return max([dp(i) for i in range(len(nums))])