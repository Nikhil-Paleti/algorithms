# topics: graph, uf

class UF:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False  # no merge (already connected)

        # union by rank
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1

        self.components -= 1
        return True  # merged

    def all_connected(self) -> bool:
        return self.components == 1

class Solution:
    def earliestAcq(self, logs: list[list[int]], n: int) -> int:
        # Sort by timestamp!
        logs.sort(key=lambda x: x[0])

        uf = UF(n)
        for t, i, j in logs:
            uf.union(i, j)
            if uf.all_connected():
                return t
        return -1