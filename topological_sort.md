# Topological Sort — Kahn’s Algorithm & DFS-Based Method

## Overview
**Topological sort** is a linear ordering of the vertices of a **Directed Acyclic Graph (DAG)** such that for every edge `u → v`, `u` appears before `v` in the ordering.

Two standard algorithms:
1. **Kahn’s Algorithm** (BFS with in-degrees)
2. **DFS-Based Topological Sort** (postorder on a DAG)

Both run in **O(V + E)** time and **O(V + E)** space.

---

## 1) Kahn’s Algorithm (BFS with In-Degrees)

### Intuition
- A node with **in-degree = 0** has no prerequisites; it can safely appear next.
- Remove it and decrement in-degrees of its neighbors; newly freed nodes (now 0) become eligible.
- Repeat until you process all nodes. If some nodes remain with positive in-degree, the graph has a **cycle** (no topological order).

### Python Implementation
```python
from collections import defaultdict, deque
from typing import List

def kahn_toposort(n: int, edges: List[List[int]]) -> List[int]:
    graph = defaultdict(list)
    indegree = [0] * n

    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1

    q = deque([i for i in range(n) if indegree[i] == 0])
    topo = []

    while q:
        u = q.popleft()
        topo.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)

    return topo if len(topo) == n else []  # empty => cycle detected
```

---

## 2) DFS-Based Topological Sort (Postorder)

### Intuition
- Visit nodes via DFS; after you finish exploring all descendants of `u`, add `u` to a list.
- Reversing that postorder list yields a topological order.
- Must ensure the graph has **no directed cycles**; use **3-color DFS** (unvisited/visiting/done) to detect cycles.

### Python Implementation
```python
from collections import defaultdict
from typing import List

def dfs_toposort(n: int, edges: List[List[int]]) -> List[int]:
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    state = [0] * n  # 0=unvisited, 1=visiting, 2=done
    order = []
    has_cycle = False

    def dfs(u: int):
        nonlocal has_cycle
        if has_cycle:
            return
        if state[u] == 1:  # back-edge => cycle
            has_cycle = True
            return
        if state[u] == 2:
            return

        state[u] = 1
        for v in graph[u]:
            dfs(v)
        state[u] = 2
        order.append(u)

    for u in range(n):
        if state[u] == 0:
            dfs(u)
            if has_cycle:
                return []  # no topo order if cycle

    return order[::-1]
```

---

## 3) Kahn vs DFS — When to Use Which?

| Aspect | Kahn’s Algorithm | DFS-Based |
|---|---|---|
| Style | Iterative (BFS on in-degrees) | Recursive (postorder) |
| Cycle Detection | Natural (size check) | 3-color/back-edge |
| Lexicographic Control | Easy (use min-heap for 0-in-degree set) | Harder (need sorted adjacency + stack discipline) |
| Memory | Queue + in-degree | Recursion stack + adjacency |
| Multi-Source | Natural (all 0-in-degree nodes) | Fine (run DFS from each unvisited) |
| Unique Order Check | Easy (check if queue size ever > 1) | Non-trivial |

---

## 4) Example: Course Schedule II (LC 210)

### Using Kahn
```python
def findOrder(numCourses, prerequisites):
    from collections import defaultdict, deque

    graph = defaultdict(list)
    indeg = [0] * numCourses
    for a, b in prerequisites:      # b -> a
        graph[b].append(a)
        indeg[a] += 1

    q = deque([i for i in range(numCourses) if indeg[i] == 0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    return order if len(order) == numCourses else []
```

### Using DFS
```python
def findOrder(numCourses, prerequisites):
    from collections import defaultdict

    graph = defaultdict(list)
    for a, b in prerequisites:  # b -> a
        graph[b].append(a)

    state = [0] * numCourses
    order = []
    has_cycle = False

    def dfs(u):
        nonlocal has_cycle
        if state[u] == 1:
            has_cycle = True
            return
        if state[u] == 2:
            return
        state[u] = 1
        for v in graph[u]:
            dfs(v)
        state[u] = 2
        order.append(u)

    for u in range(numCourses):
        if state[u] == 0:
            dfs(u)
            if has_cycle:
                return []
    return order[::-1]
```

---

## 5) Cheatsheet

- **Cycle detection only**:  
  - Kahn: if topo list < V.  
  - DFS: if you find a back-edge (state=visiting).  

- **Need lexicographically smallest topo order**:  
  - Use **Kahn + min-heap** instead of deque.  
  ```python
  import heapq
  pq = [i for i in range(n) if indegree[i] == 0]
  heapq.heapify(pq)
  topo = []
  while pq:
      u = heapq.heappop(pq)  # smallest available node
      topo.append(u)
      for v in graph[u]:
          indegree[v] -= 1
          if indegree[v] == 0:
              heapq.heappush(pq, v)
  ```

- **Need to check if topo order is unique**:  
  - In Kahn’s algorithm, if the queue (or heap) ever contains more than one node, then the ordering is **not unique**.

- **Which to pick?**  
  - Prefer **Kahn** if you want an iterative approach, cycle detection, lexicographic control, or uniqueness check.  
  - Prefer **DFS** if recursion is natural, or you’re already using DFS for cycle detection.  

---

## 6) Practice Prompts
- Course Schedule I & II (LeetCode 207, 210)  
- Alien Dictionary (LeetCode 269)  
- Build System / Package Installation order  
- Task Scheduling with prerequisites  

---
