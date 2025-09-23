# topics: dp

from functools import lru_cache

class Solution:
    def minDifficulty(self, jobDifficulty: list[int], d: int) -> int:
        n = len(jobDifficulty)
        if n < d:
            return -1

        @lru_cache(None)
        def dp(i: int, day: int) -> int:
            if day == d:
                return max(jobDifficulty[i:])

            remaining_days = d - day
            max_jobs_today = n - i - remaining_days

            best = float('inf')
            today_max = 0
            for j in range(i, i + max_jobs_today):
                today_max = max(today_max, jobDifficulty[j])
                best = min(best, today_max + dp(j + 1, day + 1))
            return best

        return dp(0, 1)