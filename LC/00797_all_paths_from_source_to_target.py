# topics: graph, dfs

class Solution:
    def allPathsSourceTarget(self, graph: list[list[int]]) -> list[list[int]]:
        n = len(graph)
        paths = []
        path = [0]
        # 0 to n-1 
        def dfs(v):
            if v == n-1:
                paths.append(path.copy())
            for nei in graph[v]:
                path.append(nei)
                dfs(nei)
                path.pop()
        
        dfs(0)

        return paths        