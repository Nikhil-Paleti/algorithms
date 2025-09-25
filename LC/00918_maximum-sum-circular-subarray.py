# topics: dp

class Solution:
    def maxSubarraySumCircular(self, nums: List[int]) -> int:
        total_sum = 0
        current_max = 0
        max_sum_center = float('-inf')
        current_min = 0
        min_sum_center = float('inf')

        for n in nums:
            total_sum += n
            current_max = max(current_max + n, n)
            current_min = min(current_min + n, n)
            max_sum_center = max(current_max, max_sum_center)
            min_sum_center = min(current_min, min_sum_center)
        
        if max_sum_center < 0:
            return max_sum_center
            
        outer_sum = total_sum - min_sum_center
        ans = max(max_sum_center, outer_sum)
        return ans
