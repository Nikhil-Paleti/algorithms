# Minimum Spanning Trees — Prim’s & Kruskal’s Algorithms

## 1. What is a Minimum Spanning Tree (MST)?
- A **spanning tree** of a graph is a subset of edges that connects all vertices without cycles.  
- A **minimum spanning tree** is a spanning tree with the **minimum total edge weight**.  
- MSTs are defined for **connected, undirected, weighted graphs**.  
- If edge weights are unique, the MST is unique; otherwise, multiple MSTs may exist with the same weight.

---

## 2. Prim’s Algorithm

### Purpose
Greedy algorithm that grows the MST from an arbitrary starting vertex, always adding the minimum-weight edge that connects a new vertex to the existing tree.

### Intuition
- Very similar to **Dijkstra’s algorithm**, but instead of minimizing path distance, we minimize the cost to connect a new node to the tree.
- Always keep track of the cheapest edge from the tree to any node outside.

### Steps
1. Pick an arbitrary start node.  
2. Put all its edges into a min-heap (priority queue).  
3. Repeatedly extract the smallest edge `(u, v)`:
   - If `v` is already in the MST, skip it.
   - Otherwise, add `(u, v)` to the MST and push all edges from `v`.  
4. Stop when all vertices are included.

### Python Implementation
```python
import heapq
from collections import defaultdict
from typing import List, Tuple

def prims(n: int, edges: List[Tuple[int, int, int]]) -> int:
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((w, v))
        graph[v].append((w, u))

    visited = set()
    min_heap = [(0, 0)]  # (weight, node)
    total_cost = 0

    while len(visited) < n:
        w, u = heapq.heappop(min_heap)
        if u in visited:
            continue
        visited.add(u)
        total_cost += w
        for nw, v in graph[u]:
            if v not in visited:
                heapq.heappush(min_heap, (nw, v))

    return total_cost
```

### Complexity
- **Time:** `O(E log V)` (heap operations dominate).  
- **Space:** `O(V + E)`.

---

## 3. Kruskal’s Algorithm

### Purpose
Greedy algorithm that builds the MST by sorting edges by weight and adding them one by one, skipping edges that form cycles.

### Intuition
- Start with all nodes as separate components.  
- Repeatedly add the lightest edge that connects two different components.  
- Use **Union-Find (Disjoint Set Union, DSU)** to detect cycles.

### Steps
1. Sort all edges by weight.  
2. Initialize Union-Find (each vertex its own set).  
3. For each edge `(u, v, w)` in sorted order:
   - If `u` and `v` are in different sets, union them and add `w` to total.  
   - Otherwise skip (to avoid cycle).  
4. Stop when we have `V-1` edges.

### Python Implementation
```python
def kruskal(n: int, edges: List[Tuple[int, int, int]]) -> int:
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            parent[rx] = ry
        elif rank[rx] > rank[ry]:
            parent[ry] = rx
        else:
            parent[ry] = rx
            rank[rx] += 1
        return True

    edges.sort(key=lambda x: x[2])
    total_cost = 0
    for u, v, w in edges:
        if union(u, v):
            total_cost += w
    return total_cost
```

### Complexity
- **Sorting edges:** `O(E log E)`.  
- **Union-Find operations:** ~`O(α(V))` (inverse Ackermann, nearly constant).  
- **Total:** `O(E log E)`.

---

## 4. Comparison

| Feature            | Prim’s Algorithm          | Kruskal’s Algorithm        |
|--------------------|---------------------------|----------------------------|
| Approach           | Grow from a starting node | Sort edges, pick smallest  |
| Data structure     | Min-heap (priority queue) | Union-Find (DSU)           |
| Best for           | Dense graphs (E ~ V²)     | Sparse graphs (E ~ V)      |
| Complexity         | O(E log V)                | O(E log E) ≈ O(E log V)    |
| Similar to         | Dijkstra’s algorithm      | Greedy + Union-Find        |

---

## 5. Example

Graph (undirected, weighted):  
```
n = 4
edges = [
    (0, 1, 10),
    (0, 2, 6),
    (0, 3, 5),
    (1, 3, 15),
    (2, 3, 4)
]
```

- **Kruskal**: Sort → pick (2,3,4), (0,3,5), (0,1,10). Total = 19.  
- **Prim**: Start at 0 → pick (0,3,5), then (2,3,4), then (0,1,10). Total = 19.  

Both return MST cost = 19.

---

## 6. Typical Problems
- **Network design:** connect computers/routers with minimum cable cost.  
- **Road planning:** build roads with least total cost while keeping all cities connected.  
- **Clustering:** use MST to partition a graph into clusters by removing the largest edges.  
- **LeetCode examples:**  
  - [1135. Connecting Cities With Minimum Cost](https://leetcode.com/problems/connecting-cities-with-minimum-cost/)  
  - [1584. Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/)  

---

## 7. Key Takeaways
- Both Prim’s and Kruskal’s are greedy algorithms that solve MST.  
- Use **Prim’s** when graph is dense (works well with adjacency lists + heap).  
- Use **Kruskal’s** when graph is sparse (sorting edges is efficient).  
- Union-Find is central to Kruskal; Min-heap is central to Prim.  
