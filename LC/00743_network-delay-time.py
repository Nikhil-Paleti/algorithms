# topics: graph, dijkstra

import heapq
from typing import List 
from collections import defaultdict

class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:

        graph = defaultdict(list)
        for u,v,w in times:
            graph[u].append((v,w))

        dist = [float('inf')] * (n + 1)
        dist[k] = 0
        heap = [(0, k)]
        
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for v, w in graph[u]:
                if dist[v] > d + w:
                    dist[v] = d + w
                    heapq.heappush(heap, (dist[v], v))

        ans = max(dist[1:])
        return ans if ans != float('inf') else -1

        