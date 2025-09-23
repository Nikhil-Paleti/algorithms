# topics: dp, bit manipulation

from typing import List 
from functools import lru_cache
class Solution:
    def maxStudents(self, seats: List[List[str]]) -> int:
        m = len(seats)
        n = len(seats[0])

        @lru_cache(None)
        def dp(i, mask):
            if i == m:
                return 0
            
            current_row = 0
            for idx, col in enumerate(seats[i]):
                if col == ".":
                    current_row = current_row | (1 << idx)
            
            val = 0
            for arrangement in range(1 << n):
                if (arrangement & current_row) != arrangement:
                    continue

                if (arrangement & (arrangement << 1)) != 0:
                    continue

                # check diagnoal cheating 
                if (arrangement & (mask << 1)) != 0:
                    continue
                if (arrangement & (mask >> 1)) != 0:
                    continue 

                count = arrangement.bit_count()

                val = max(val, count + dp(i+1, arrangement))

            return val
        
        return dp(0, 0)
        