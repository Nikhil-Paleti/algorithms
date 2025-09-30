# Single-Source & All-Pairs Shortest Path Algorithms — Notes

## 1. Dijkstra’s Algorithm

### Purpose
Finds the **shortest path distances** from a single source to all other nodes in a weighted graph with **non-negative edge weights**.

### Core Idea
- Greedy approach using a priority queue (min-heap).
- Always expand the node with the smallest known distance so far.
- Update (relax) neighbors if a shorter path is found.

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
- Cannot handle **negative edge weights**.
- Cannot detect negative cycles.
- Works best for sparse graphs; in dense graphs, Floyd–Warshall may be better.

---

## 2. Bellman–Ford Algorithm

### Purpose
Finds the **shortest path distances** from a single source to all other nodes in a weighted graph, allowing **negative edge weights**.  
Also detects **negative weight cycles**.

### Core Idea
- Relax all edges **V-1 times**.
- If an edge can still be relaxed on the V-th pass, a negative cycle exists.

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
- Slower than Dijkstra.
- In dense graphs with large V, may be too slow.
- Detects but does not directly return the cycle (though can be extended).

---

## 3. Floyd–Warshall Algorithm

### Purpose
Computes the **shortest path distances between all pairs of nodes** in a weighted graph.  
Works with negative weights, but **not with negative cycles**.

### Core Idea
- Dynamic programming approach.  
- Iteratively allow intermediate nodes to be part of paths.  
- Transition:  
  dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

### Python Implementation
```python
def floyd_warshall(n, dist):
    # dist is an adjacency matrix (∞ if no edge, 0 on diagonal)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
```

### Complexity
- **Time:** O(V³)  
- **Space:** O(V²)

### Limitations
- Too slow for very large graphs.  
- Cannot handle negative cycles (dist[i][i] < 0 indicates one).

---

## 4. Dijkstra vs Bellman–Ford vs Floyd–Warshall

| Feature            | Dijkstra                        | Bellman–Ford                 | Floyd–Warshall        |
|--------------------|---------------------------------|------------------------------|-----------------------|
| Edge weights       | Non-negative only               | Negative allowed             | Negative allowed      |
| Negative cycles    | Not detectable                  | Detects                      | Detects (dist[i][i]<0)|
| Problem type       | Single-source shortest paths     | Single-source shortest paths | All-pairs shortest paths |
| Time complexity    | O((V+E) log V)                  | O(V * E)                     | O(V³)                 |
| Space complexity   | O(V + E)                        | O(V)                         | O(V²)                 |
| Best for           | Sparse graphs, positive weights | Graphs w/ negative edges     | Small/medium dense graphs |
