# Dijkstra’s Algorithm & Bellman–Ford Algorithm — Notes

## 1. Dijkstra’s Algorithm

### Purpose
Finds the **shortest path distances** from a single source to all other nodes in a weighted graph with **non-negative edge weights**.

### Core Idea
- Greedy approach using a priority queue (min-heap).
- Always expand the node with the smallest known distance so far.
- Update (relax) neighbors if a shorter path is found.

### Pseudocode
1. Initialize `dist[source] = 0`, all others = infinity.
2. Push `(0, source)` into a min-heap.
3. While heap not empty:
   - Pop `(d, u)`.
   - If `d > dist[u]`, skip (outdated entry).
   - For each `(u, v, w)`:
     - If `dist[v] > dist[u] + w`: update and push new distance.

### Python Implementation
```python
import heapq
from collections import defaultdict

def dijkstra(n, edges, source):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))

    dist = [float('inf')] * n
    dist[source] = 0
    heap = [(0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[v] > d + w:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist
```

### Complexity
- **Time:** O((V + E) log V) with a binary heap.
- **Space:** O(V + E).

### Limitations
- Cannot handle **negative edge weights** (because greedy property breaks).
- Cannot detect negative cycles.
- Works best for sparse graphs; in dense graphs, Floyd–Warshall may be better.

### Typical Problems
- Shortest path from a single source in road networks, graphs with positive weights.
- Variants:
  - Shortest path tree construction.
  - K-shortest paths (slight modification).
  - Shortest path with extra conditions (e.g., limited stops).

---

## 2. Bellman–Ford Algorithm

### Purpose
Finds the **shortest path distances** from a single source to all other nodes in a weighted graph, allowing **negative edge weights**.  
Also detects **negative weight cycles**.

### Core Idea
- Dynamic programming style.
- Relax all edges **V-1 times** (longest simple path has at most V-1 edges).
- One more relaxation: if any distance improves, then a negative cycle exists.

### Pseudocode
1. Initialize `dist[source] = 0`, all others = infinity.
2. Repeat V-1 times:
   - For each edge (u, v, w):
     - If `dist[v] > dist[u] + w`: update `dist[v]`.
3. Run one more pass:
   - If any distance can be updated → negative cycle.

### Python Implementation
```python
def bellman_ford(n, edges, source):
    dist = [float('inf')] * n
    dist[source] = 0

    # Relax edges V-1 times
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[v] > dist[u] + w:
                dist[v] = dist[u] + w

    # Check for negative cycles
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[v] > dist[u] + w:
            return None, True  # Negative cycle detected

    return dist, False
```

### Complexity
- **Time:** O(V * E).
- **Space:** O(V).

### Limitations
- Slower than Dijkstra (O(V * E) vs O((V+E) log V)).
- In dense graphs with large V, may be too slow.
- Detects but does not return the exact negative cycle path (though can be extended to do so).

### Typical Problems
- Graphs with negative weights (e.g., currency arbitrage, stock trading).
- Detecting negative weight cycles.
- Solving systems where edge weights represent constraints.

---

## 3. Dijkstra vs Bellman–Ford

| Feature            | Dijkstra                   | Bellman–Ford              |
|--------------------|---------------------------|---------------------------|
| Edge weights       | Non-negative only          | Negative allowed          |
| Negative cycles    | Not detectable             | Detects negative cycles   |
| Time complexity    | O((V+E) log V) (with heap)| O(V * E)                 |
| Space complexity   | O(V + E)                  | O(V)                     |
| Graph density      | Works best for sparse      | Works, but slower         |

---

## 4. Types of Problems & Applications

### For Dijkstra
- Network routing protocols (OSPF, shortest paths in IP routing).
- GPS navigation, road networks.
- Any non-negative weighted shortest path problem.

### For Bellman–Ford
- Detecting **negative cycles** (arbitrage detection in currency exchange).
- General shortest paths when weights may be negative.
- Used in distance-vector routing protocols (like RIP).

### Problem Variants
- **Shortest path queries**: from single source to all nodes.
- **Path reconstruction**: keep parent pointers.
- **Negative cycle detection**: Bellman–Ford specific.
- **All-pairs shortest path**: run Dijkstra from every node (if no negatives) or use Floyd–Warshall.
- **Special constraints**: e.g., limit on number of edges → Bellman–Ford naturally handles this (DP style).

---

## 5. Key Takeaways
- Use **Dijkstra** when all edges are non-negative and performance matters.
- Use **Bellman–Ford** when negative edges exist, or when negative cycle detection is required.
- Both are **single-source shortest path algorithms**, but with different strengths.
- Bellman–Ford is more general but slower; Dijkstra is faster but limited.

---

# Negative Cycle Detection and Retrieval (Bellman–Ford Variant)

## 1. Idea

We want not only to detect a negative cycle but also to **return the actual cycle**.  
This is a standard extension of the Bellman–Ford algorithm.

Steps:

1. Add a **virtual source** with 0-weight edges to every node.  
   → ensures we can detect cycles in any component of the graph.

2. Run Bellman–Ford for `V` passes (instead of `V-1`).  
   - If any edge relaxes on the `V`-th pass, the updated vertex `x` is on or can reach a negative cycle.

3. From that vertex, move back `V` times using parent pointers.  
   - This guarantees that you land **inside the cycle** (not just near it).

4. From that node, walk parent pointers until you return to the start.  
   - This sequence of nodes is a negative cycle.

---

## 2. Python Implementation

```python
from typing import List, Tuple, Optional

def find_negative_cycle(n: int, edges: List[Tuple[int, int, float]]) -> Optional[List[int]]:
    """
    Find and return one negative cycle as a list of vertices in order.
    Graph is directed. Vertices are 0..n-1.
    Edges: list of (u, v, w).
    Returns: list of vertices forming a cycle [u0, u1, ..., uk-1, u0],
             or None if no negative cycle exists.
    """
    INF = float('inf')
    dist = [0.0] * n          # start with 0 for all, simulating a super-source
    parent = [-1] * n

    x = -1
    for i in range(n):
        x = -1
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                x = v
        if x == -1:  # no update in this pass
            break

    if x == -1:
        return None  # no negative cycle

    # Step 1: move x back n times to ensure it's inside the cycle
    for _ in range(n):
        x = parent[x]

    # Step 2: collect the cycle
    cycle = []
    cur = x
    while True:
        cycle.append(cur)
        cur = parent[cur]
        if cur == x or cur == -1:
            break

    if cur == -1:
        return None  # failed reconstruction (should not happen)

    cycle.reverse()
    return cycle