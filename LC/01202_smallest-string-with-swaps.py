# topics: graph, uf

from collections import defaultdict
from typing import List

class UF:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1
        return True

class Solution:
    def smallestStringWithSwaps(self, s: str, pairs: List[List[int]]) -> str:
        n = len(s)
        uf = UF(n)
        for i, j in pairs:
            uf.union(i, j)

        # 1) Group indices by component root
        comp = defaultdict(list)
        roots = [uf.find(i) for i in range(n)]  # cache roots once
        for i, r in enumerate(roots):
            comp[r].append(i)

        res = list(s)
        # 2) For each component, sort indices and the chars for those indices,
        #    then place smallest chars at smallest indices.
        for idxs in comp.values():
            idxs.sort()
            chars = sorted(s[i] for i in idxs)
            for i, ch in zip(idxs, chars):
                res[i] = ch

        return "".join(res)