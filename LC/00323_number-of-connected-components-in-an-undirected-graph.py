# topics: graph, uf

class UF:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, n):
        if n != self.parent[n]:
            self.parent[n] = self.find(self.parent[n])
        return self.parent[n]
    
    def union(self, n1, n2):
        r1, r2 = self.find(n1), self.find(n2)
        if r1 == r2:
            return False
        
        if self.rank[r1] > self.rank[r2]:
            self.parent[r2] = r1
        elif self.rank[r2] > self.rank[r1]:
            self.parent[r1] = r2
        else:
            self.parent[r2] = r1
            self.rank[r1] += 1
        
        return True

class Solution:
    def countComponents(self, n: int, edges: list[list[int]]) -> int:
        uf = UF(n)
        for i, j in edges:
            uf.union(i, j)
        
        components = set()
        for i in range(n):
            components.add(uf.find(i))
        
        return len(components)
        