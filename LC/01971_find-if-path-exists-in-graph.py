# topics: graph, dfs

from collections import defaultdict

class Solution:
    def validPath(self, n: int, edges: list[list[int]], source: int, destination: int) -> bool:
        if source == destination:
            return True
            
        adj = defaultdict(list)
        for i,j in edges:
            adj[i].append(j)
            adj[j].append(i)
        
        visited = {source}
        stack = [source]
        
        while stack:
            node = stack.pop()
            for nei in adj[node]:
                if nei in visited:
                    continue
                if nei == destination:
                    return True
                stack.append(nei)
                visited.add(nei)
                
        return False
        