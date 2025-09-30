# Union-Find (Disjoint Set Union - DSU)

Union-Find (also called DSU) is a data structure that keeps track of a partition of a set into disjoint subsets.  
It supports two main operations efficiently:

1. **Find(x):** Determine which subset a particular element `x` belongs to.  
2. **Union(x, y):** Merge the subsets containing `x` and `y`.

To make it efficient, we use two optimizations:
- **Path Compression** in `find` → flattens the structure for fast lookups.  
- **Union by Rank/Size** in `union` → attach smaller tree under larger tree.

---

## Implementation (with Path Compression + Union by Rank)

```python
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n   # rank ~ tree height

    def find(self, x: int) -> int:
        # Find with path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        # Union by rank. Returns True if unioned, False if already in same set.
        rootX, rootY = self.find(x), self.find(y)
        if rootX == rootY:
            return False

        if self.rank[rootX] < self.rank[rootY]:
            self.parent[rootX] = rootY
        elif self.rank[rootX] > self.rank[rootY]:
            self.parent[rootY] = rootX
        else:
            self.parent[rootY] = rootX
            self.rank[rootX] += 1
        return True
```

---

## Complexity
- **Find:** Amortized O(α(n)), where α is the inverse Ackermann function (practically ≤ 4).  
- **Union:** Amortized O(α(n)).  
- **Space:** O(n).

---

## Example LeetCode Usage

### LeetCode 684 — Redundant Connection
Find an extra edge that forms a cycle in a tree-like graph.

```python
from typing import List

class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        uf = UnionFind(n+1)
        for u, v in edges:
            if not uf.union(u, v):
                return [u, v]
        return []
```

---

## Key Takeaways
- Use **path compression** in `find` → speeds up queries.  
- Use **union by rank/size** → prevents tall trees.  
- Amortized almost-constant time per operation.  
- Very common in graph problems: connected components, MST (Kruskal), cycle detection.
