# DFS with 3-Color (State Marking) — Notes

## 1. What is the 3-Color Method?
A DFS-based technique to detect **cycles in a directed graph** and to memoize validity of nodes.

Each node is assigned one of three states:
- **0 = unvisited** (not seen yet)
- **1 = visiting** (currently in the recursion stack)
- **2 = done** (fully processed and safe)

---

## 2. Core Idea
- When entering a node in DFS, mark it as **visiting (1)**.
- If you ever encounter a **visiting** node again during recursion, you found a **cycle**.
- When all neighbors of a node are processed successfully, mark it **done (2)**.
- If you revisit a **done** node, you can safely reuse the result (memoization).

This prevents infinite recursion and ensures each node is processed at most once.

---

## 3. Standard Cycle Detection (Directed Graph)
```python
def hasCycle(adj, n):
    state = [0] * n  # 0=unvisited, 1=visiting, 2=done

    def dfs(u):
        if state[u] == 1:
            return True       # cycle detected
        if state[u] == 2:
            return False      # already checked

        state[u] = 1          # mark visiting
        for v in adj[u]:
            if dfs(v):
                return True
        state[u] = 2          # mark done
        return False

    for u in range(n):
        if state[u] == 0 and dfs(u):
            return True
    return False
```

- **Time Complexity:** O(V + E)  
- **Space Complexity:** O(V + E) for adjacency and recursion

---

## 4. Application: Topological Sort
- If no cycle is found, DFS postorder gives a valid topological order.
- Cycle detection step = same 3-color method.

```python
def topoSort(adj, n):
    state = [0] * n
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
        for v in adj[u]:
            dfs(v)
        state[u] = 2
        order.append(u)

    for u in range(n):
        if state[u] == 0:
            dfs(u)

    if has_cycle:
        return []   # no topo sort exists
    return order[::-1]
```

---

## 5. Application: "All Paths Lead to Destination" (LC 1059)
Here, we extend the 3-color method:
- Reject if destination has outgoing edges.
- Reject if any cycle is found.
- Reject if any leaf node is not the destination.

```python
from collections import defaultdict

def leadsToDestination(n, edges, source, destination):
    adj = defaultdict(list)
    for u,v in edges:
        adj[u].append(v)

    if adj[destination]:  # destination must be terminal
        return False

    state = [0] * n  # 0=unvisited, 1=visiting, 2=done

    def dfs(u):
        if state[u] == 1: return False  # cycle
        if state[u] == 2: return True   # already checked
        if not adj[u]: return u == destination

        state[u] = 1
        for v in adj[u]:
            if not dfs(v):
                return False
        state[u] = 2
        return True

    return dfs(source)
```

---

## 6. Key Takeaways
- **3-color DFS** is a versatile template for:
  - Cycle detection in directed graphs.
  - Validity checks in path problems (e.g., LC 1059).
  - Topological sorting.
- Colors (states) ensure:
  - No infinite recursion.
  - Each node is processed only once.
  - Easy memoization of results.

---
