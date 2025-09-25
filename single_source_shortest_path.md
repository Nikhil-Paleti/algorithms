# Single-Source Shortest Path Algorithms — Notes

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

## 3. Shortest Path Faster Algorithm (SPFA)

### Purpose
An optimization of the **Bellman–Ford algorithm** for single-source shortest paths.  
It uses a **queue** to process only the vertices that could potentially improve their neighbors, rather than blindly relaxing all edges `V-1` times.

### Core Idea
- Initialize distances like Bellman–Ford.
- Put the source into a queue.
- While queue is not empty:
  - Pop a vertex `u`.
  - For each edge `(u, v, w)`:
    - If `dist[v] > dist[u] + w`, update `dist[v]`.
    - If `v` is not in the queue, push it.

This often reduces unnecessary relaxations in practice.

### Python Implementation
```python
from collections import deque
from typing import List, Tuple

def spfa(n: int, edges: List[Tuple[int, int, float]], source: int):
    INF = float("inf")
    dist = [INF] * n
    in_queue = [False] * n
    count = [0] * n  # number of times each node was relaxed (for cycle detection)

    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    dist[source] = 0
    q = deque([source])
    in_queue[source] = True

    while q:
        u = q.popleft()
        in_queue[u] = False
        for v, w in graph[u]:
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                count[v] += 1
                if count[v] >= n:
                    return None, True  # negative cycle detected
                if not in_queue[v]:
                    q.append(v)
                    in_queue[v] = True

    return dist, False
```

### Complexity
- **Worst case:** O(V * E) (same as Bellman–Ford).
- **Average case (on many sparse graphs):** close to O(E) in practice.
- **Space:** O(V + E).

### Limitations
- SPFA can degrade to **O(V * E)** in adversarial graphs (especially dense graphs or those with many negative edges).
- Same as Bellman–Ford, cannot produce valid shortest paths in the presence of negative cycles.

### Typical Problems
- Used as a practical improvement over Bellman–Ford in many real-world routing systems.
- Detecting negative cycles while being faster in sparse cases.
- Still relevant in competitive programming (though considered “unsafe” in worst-case constraints).

### Key Takeaways
- SPFA is a **queue-based improvement** over Bellman–Ford.
- Faster in many real-world cases (especially sparse graphs).
- Worst-case time is still **O(V * E)**, so it’s not strictly better in theory.

---

## 4. Dijkstra vs Bellman–Ford vs SPFA

| Feature            | Dijkstra                   | Bellman–Ford              | SPFA (queue-based)       |
|--------------------|---------------------------|---------------------------|--------------------------|
| Edge weights       | Non-negative only          | Negative allowed          | Negative allowed         |
| Negative cycles    | Not detectable             | Detects negative cycles   | Detects negative cycles  |
| Time complexity    | O((V+E) log V) (with heap)| O(V * E)                 | O(V * E) worst, ~O(E) avg|
| Space complexity   | O(V + E)                  | O(V)                     | O(V + E)                 |
| Graph density      | Works best for sparse      | Works, but slower         | Best for sparse (avg)    |

---

## 5. Negative Cycle Detection and Retrieval (Bellman–Ford Variant)

### Idea
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

### Python Implementation
```python
from typing import List, Tuple, Optional

def find_negative_cycle(n: int, edges: List[Tuple[int, int, float]]) -> Optional[List[int]]:
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
```

### Example
```python
# Graph with a negative cycle: 0 -> 1 -> 2 -> 0 with total weight -3
n = 3
edges = [
    (0, 1, 1),
    (1, 2, 1),
    (2, 0, -5)
]

cycle = find_negative_cycle(n, edges)
print(cycle)  # Output: [0, 1, 2]
```

This corresponds to the negative cycle **0 → 1 → 2 → 0**.

### Complexity
- **Time Complexity:** O(V * E) (same as Bellman–Ford).
- **Space Complexity:** O(V).

### Notes and Extensions
- Works for **directed graphs**.  
- Returns **one** negative cycle. Enumerating *all* negative cycles is more complex.
- If you want **edges** instead of vertices: collect `(parent[v], v)` while reconstructing.
- Distances to nodes reachable from a negative cycle are effectively **-∞**, so shortest paths aren’t well-defined.

### Applications
- **Currency arbitrage:** detect cycles in exchange-rate graphs where the product of exchange rates < 1.
- **Constraint systems:** detect infeasible systems of difference constraints.
- **Optimization:** check whether cost functions can be decreased indefinitely.

---
