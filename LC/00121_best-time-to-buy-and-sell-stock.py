# topics: dp

class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        min_stock = prices[0]
        profit = 0
        for p in prices:
            min_stock = min(min_stock, p)
            profit = max(profit, p-min_stock)
        
        return profit