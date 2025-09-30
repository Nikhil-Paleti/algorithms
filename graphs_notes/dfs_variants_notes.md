
# DFS Variants — Python Cheat Sheet

> A grab‑bag of depth‑first strategies you’ll likely need in interviews & practice. Each snippet is **minimal**, focuses on the DFS core, and can be pasted as-is. Graphs are assumed to be adjacency lists unless noted. Trees use a simple `TreeNode`.

---

## 0) Minimal Graph Helpers

```python
from collections import defaultdict, deque
from typing import List, Dict, Set, Tuple, Optional

# Build an undirected or directed graph
def build_graph(edges: List[Tuple[int,int]], directed=False) -> Dict[int, List[int]]:
    g = defaultdict(list)
    for u,v in edges:
        g[u].append(v)
        if not directed:
            g[v].append(u)
    return g
```

---

## 1) Recursive DFS (graph)

```python
def dfs_recursive(g: Dict[int, List[int]], u: int, seen: Set[int]):
    seen.add(u)
    # process u (preorder spot)
    for v in g[u]:
        if v not in seen:
            dfs_recursive(g, v, seen)
    # process u (postorder spot)

# usage
# g = build_graph([...], directed=False)
# seen = set()
# dfs_recursive(g, start_node, seen)
```

---

## 2) Iterative DFS with explicit stack (graph)

```python
def dfs_iterative(g: Dict[int, List[int]], start: int):
    seen = set([start])
    stack = [start]
    while stack:
        u = stack.pop()
        # process u
        for v in g[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
```

---

## 3) DFS Traversal Orders on a Tree (pre/in/post)

```python
class TreeNode:
    def __init__(self, val=0, left: 'TreeNode'=None, right: 'TreeNode'=None):
        self.val = val
        self.left = left
        self.right = right

def preorder(root: Optional[TreeNode]) -> List[int]:
    res = []
    def dfs(node):
        if not node: return
        res.append(node.val)           # pre
        dfs(node.left)
        dfs(node.right)
    dfs(root); return res

def inorder(root: Optional[TreeNode]) -> List[int]:
    res = []
    def dfs(node):
        if not node: return
        dfs(node.left)
        res.append(node.val)           # in
        dfs(node.right)
    dfs(root); return res

def postorder(root: Optional[TreeNode]) -> List[int]:
    res = []
    def dfs(node):
        if not node: return
        dfs(node.left)
        dfs(node.right)
        res.append(node.val)           # post
    dfs(root); return res
```

---

## 4) 3‑Color DFS (WHITE/GRAY/BLACK) for cycle detection (directed)

```python
WHITE, GRAY, BLACK = 0, 1, 2

def has_cycle_directed(g: Dict[int, List[int]]) -> bool:
    color = {u: WHITE for u in g}
    def dfs(u):
        color[u] = GRAY
        for v in g[u]:
            if color[v] == GRAY:     # back edge
                return True
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False
    return any(dfs(u) for u in list(g) if color[u] == WHITE)
```

---

## 5) Topological Sort via DFS postorder (DAG only)

```python
def topo_sort(g: Dict[int, List[int]]) -> List[int]:
    color = {u: 0 for u in g}  # 0=unseen,1=visiting,2=done
    order = []
    cycle = False
    def dfs(u):
        nonlocal cycle
        color[u] = 1
        for v in g[u]:
            if color[v] == 1:
                cycle = True
                return
            if color[v] == 0:
                dfs(v)
                if cycle: return
        color[u] = 2
        order.append(u) # postorder
    for u in list(g):
        if color[u] == 0:
            dfs(u)
            if cycle: return []  # cycle => no topo order
    return order[::-1]
```

---

## 6) Discovery / Finish Times (timestamps)

```python
def dfs_times(g: Dict[int, List[int]]):
    time = 0
    tin, tout = {}, {}
    seen = set()
    def dfs(u):
        nonlocal time
        seen.add(u)
        time += 1; tin[u] = time
        for v in g[u]:
            if v not in seen:
                dfs(v)
        time += 1; tout[u] = time
    for u in list(g):
        if u not in seen:
            dfs(u)
    return tin, tout
```

---

## 7) Connected Components (undirected)

```python
def connected_components(g: Dict[int, List[int]]) -> List[List[int]]:
    seen, comps = set(), []
    def dfs(u, buf):
        seen.add(u); buf.append(u)
        for v in g[u]:
            if v not in seen:
                dfs(v, buf)
    for u in list(g):
        if u not in seen:
            buf = []
            dfs(u, buf)
            comps.append(buf)
    return comps
```

---

## 8) All Paths (enumeration) between s and t (DAG recommended)

```python
def all_paths(g: Dict[int, List[int]], s: int, t: int) -> List[List[int]]:
    res, path = [], []
    def dfs(u):
        path.append(u)
        if u == t:
            res.append(path.copy())
        else:
            for v in g[u]:
                dfs(v)
        path.pop()
    dfs(s)
    return res
```

---

## 9) Backtracking Template (constraints + undo)

```python
def backtrack(choices: List[int]) -> List[List[int]]:
    res, path = [], []
    used = [False]*len(choices)
    def dfs():
        # if goal reached:
        res.append(path.copy())
        # else explore:
        for i, c in enumerate(choices):
            if used[i]: continue
            # prune condition here if needed
            used[i] = True
            path.append(c)
            dfs()
            path.pop()
            used[i] = False
    dfs()
    return res
```

---

## 10) Tarjan’s SCC (lowlink on directed graph)

```python
def tarjans_scc(g: Dict[int, List[int]]) -> List[List[int]]:
    nstack, onstack = [], set()
    index, idx = {}, 0
    low = {}
    sccs = []

    def dfs(u):
        nonlocal idx
        index[u] = idx; low[u] = idx; idx += 1
        nstack.append(u); onstack.add(u)
        for v in g[u]:
            if v not in index:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif v in onstack:
                low[u] = min(low[u], index[v])
        if low[u] == index[u]:
            comp = []
            while True:
                x = nstack.pop(); onstack.remove(x)
                comp.append(x)
                if x == u: break
            sccs.append(comp)

    for u in list(g):
        if u not in index:
            dfs(u)
    return sccs
```

---

## 11) Kosaraju’s SCC (two DFS passes)

```python
def kosaraju_scc(g: Dict[int, List[int]]) -> List[List[int]]:
    order, seen = [], set()
    def dfs1(u):
        seen.add(u)
        for v in g[u]:
            if v not in seen:
                dfs1(v)
        order.append(u)
    for u in list(g):
        if u not in seen: dfs1(u)

    # reverse graph
    rg = {u: [] for u in g}
    for u in g:
        for v in g[u]:
            rg.setdefault(v, [])
            rg[v].append(u)

    seen.clear()
    comps = []
    def dfs2(u, buf):
        seen.add(u); buf.append(u)
        for v in rg[u]:
            if v not in seen:
                dfs2(v, buf)

    for u in reversed(order):
        if u not in seen:
            buf = []
            dfs2(u, buf)
            comps.append(buf)
    return comps
```

---

## 12) Articulation Points (cut vertices) — Tarjan

```python
def articulation_points(g: Dict[int, List[int]]) -> Set[int]:
    time = 0
    tin = {}
    low = {}
    seen = set()
    aps = set()

    def dfs(u, p=-1):
        nonlocal time
        seen.add(u)
        time += 1; tin[u] = low[u] = time
        child = 0
        for v in g[u]:
            if v == p: continue
            if v in seen:
                low[u] = min(low[u], tin[v])
            else:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] >= tin[u] and p != -1:
                    aps.add(u)
                child += 1
        if p == -1 and child > 1:
            aps.add(u)

    for u in list(g):
        if u not in seen:
            dfs(u)
    return aps
```

---

## 13) Bridges (critical edges) — Tarjan

```python
def bridges(g: Dict[int, List[int]]) -> List[Tuple[int,int]]:
    time = 0
    tin, low = {}, {}
    seen = set()
    out = []
    def dfs(u, p=-1):
        nonlocal time
        seen.add(u)
        time += 1; tin[u] = low[u] = time
        for v in g[u]:
            if v == p: continue
            if v in seen:
                low[u] = min(low[u], tin[v])
            else:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:
                    out.append((u, v))
    for u in list(g):
        if u not in seen: dfs(u)
    return out
```

---

## 14) Iterative Deepening DFS (IDDFS)

```python
def iddfs(g: Dict[int, List[int]], start: int, goal: int, max_depth=50) -> bool:
    def dls(u, depth, seen):
        if u == goal: return True
        if depth == 0: return False
        for v in g[u]:
            if (u, v, depth) in seen:  # optional cycle memo
                continue
            seen.add((u, v, depth))
            if dls(v, depth-1, seen):
                return True
        return False

    for depth in range(max_depth+1):
        if dls(start, depth, set()):
            return True
    return False
```

---

## 15) Randomized DFS (e.g., maze generation)

```python
import random

def randomized_dfs(g: Dict[int, List[int]], start: int) -> List[int]:
    seen, order = set(), []
    def dfs(u):
        seen.add(u); order.append(u)
        nbrs = g[u][:]
        random.shuffle(nbrs)
        for v in nbrs:
            if v not in seen:
                dfs(v)
    dfs(start)
    return order
```

---

## 16) DFS on Grid (8‑dir or 4‑dir)

```python
DIR8 = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]
DIR4 = [(1,0),(-1,0),(0,1),(0,-1)]

def dfs_grid(grid: List[List[int]], r: int, c: int, seen: Set[Tuple[int,int]]):
    R, C = len(grid), len(grid[0])
    stack = [(r,c)]
    seen.add((r,c))
    while stack:
        x,y = stack.pop()
        # process (x,y)
        for dx,dy in DIR4:
            nx, ny = x+dx, y+dy
            if 0 <= nx < R and 0 <= ny < C and (nx,ny) not in seen:
                # add any constraints here (e.g., grid[nx][ny] == 1)
                seen.add((nx,ny))
                stack.append((nx,ny))
```

---

## 17) Bipartite Check via DFS coloring (undirected)

```python
def is_bipartite(g: Dict[int, List[int]]) -> bool:
    color = {}
    def dfs(u, c) -> bool:
        color[u] = c
        for v in g[u]:
            if v not in color:
                if not dfs(v, c ^ 1):
                    return False
            elif color[v] == c:
                return False
        return True
    for u in list(g):
        if u not in color and not dfs(u, 0):
            return False
    return True
```

---

## 18) DFS with Pruning / Branch & Bound (pattern)

```python
def dfs_prune(nums: List[int], target: int) -> int:
    nums.sort(reverse=True)
    best = float('inf')

    def dfs(i, curr_sum, used):
        nonlocal best
        if curr_sum >= best: return                 # bound (prune)
        if i == len(nums):
            best = min(best, curr_sum)
            return
        # choice 1: take
        dfs(i+1, curr_sum + nums[i], used | (1<<i))
        # choice 2: skip
        dfs(i+1, curr_sum, used)
    dfs(0, 0, 0)
    return best
```

---

## 19) Subsets (power set) via DFS

```python
def subsets(nums: List[int]) -> List[List[int]]:
    res, path = [], []
    def dfs(i):
        if i == len(nums):
            res.append(path.copy()); return
        # exclude
        dfs(i+1)
        # include
        path.append(nums[i])
        dfs(i+1)
        path.pop()
    dfs(0)
    return res
```

---

## 20) Permutations via DFS

```python
def permutations(nums: List[int]) -> List[List[int]]:
    res, path = [], []
    used = [False]*len(nums)
    def dfs():
        if len(path) == len(nums):
            res.append(path.copy()); return
        for i in range(len(nums)):
            if used[i]: continue
            used[i] = True
            path.append(nums[i])
            dfs()
            path.pop()
            used[i] = False
    dfs(); return res
```

---

## 21) Combination Sum (classic DFS & dedupe pattern)

```python
def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    res, path = [], []
    candidates.sort()

    def dfs(i, remain):
        if remain == 0:
            res.append(path.copy()); return
        if remain < 0 or i == len(candidates):
            return
        # choose current (reuse allowed)
        path.append(candidates[i])
        dfs(i, remain - candidates[i])
        path.pop()
        # skip current
        dfs(i+1, remain)
    dfs(0, target)
    return res

def combination_sum2(candidates: List[int], target: int) -> List[List[int]]:
    res, path = [], []
    candidates.sort()
    def dfs(start, remain):
        if remain == 0:
            res.append(path.copy()); return
        prev = None
        for i in range(start, len(candidates)):
            if candidates[i] == prev: continue
            if candidates[i] > remain: break
            prev = candidates[i]
            path.append(candidates[i])
            dfs(i+1, remain - candidates[i])  # no reuse; dedupe by skipping equals at same depth
            path.pop()
    dfs(0, target)
    return res
```

---

## 22) Bitmask DFS (state‑space search)

```python
def tsp_like_dfs(dist: List[List[int]]) -> int:
    n = len(dist)
    from functools import lru_cache

    @lru_cache(None)
    def dfs(u: int, mask: int) -> int:
        if mask == (1<<n)-1:
            return dist[u][0]  # return to start (optional)
        best = float('inf')
        for v in range(n):
            if not (mask & (1<<v)):
                best = min(best, dist[u][v] + dfs(v, mask | (1<<v)))
        return best

    return dfs(0, 1<<0)
```

---

## 23) Bidirectional (frontier‑guided) DFS Skeleton

> True bidirectional **search** is usually BFS for shortest paths; DFS version is niche. Here’s a guarded skeleton for state‑space meet-in-the-middle style enumeration.

```python
def bidi_dfs_meet(states_from, states_to, expand):
    # states_from / states_to: sets; expand(s) -> iterable next states
    frontA, frontB = set(states_from), set(states_to)
    seenA, seenB = set(frontA), set(frontB)
    for _ in range(20):  # depth cap
        nxt = set()
        for s in frontA:
            for t in expand(s):
                if t in seenA: continue
                if t in seenB: return True
                seenA.add(t); nxt.add(t)
        frontA = nxt
        frontA, frontB = frontB, frontA  # alternate sides
        seenA, seenB = seenB, seenA
    return False
```

---

## 24) DFS with In/Out time ancestor check (tree)

```python
def euler_tour_inout(g: Dict[int, List[int]], root=0):
    tin, tout, time = {}, {}, 0
    def dfs(u, p=-1):
        nonlocal time
        time += 1; tin[u] = time
        for v in g[u]:
            if v == p: continue
            dfs(v, u)
        time += 1; tout[u] = time
    dfs(root)
    def is_ancestor(u, v):
        return tin[u] <= tin[v] and tout[v] <= tout[u]
    return tin, tout, is_ancestor
```

---

## 25) DFS for Euler Tour path listing (tree)

```python
def euler_tour_path(g: Dict[int, List[int]], root=0) -> List[int]:
    tour = []
    def dfs(u, p=-1):
        tour.append(u)             # enter
        for v in g[u]:
            if v == p: continue
            dfs(v, u)
            tour.append(u)         # backtrack
    dfs(root)
    return tour
```

---

## 26) DFS with Memoization on DAG (DP on graphs)

```python
def count_paths_dag(g: Dict[int, List[int]], s: int, t: int) -> int:
    from functools import lru_cache
    @lru_cache(None)
    def dfs(u):
        if u == t: return 1
        return sum(dfs(v) for v in g[u])
    return dfs(s)
```

---

## 27) Kahn vs DFS topo — quick reference

```python
# This section is just to remind: DFS topo uses postorder; Kahn uses indegrees + queue.
# (Kahn is BFS; included here for mental contrast.)
```

---

### Usage Tips
- Put “**work**” at the **pre** or **post** hook depending on the task.
- In graphs with cycles, guard with **visited** and/or **recursion stack**.
- For structure problems (SCC/bridges/AP), use **low‑link** patterns.
- For path enumeration, expect **exponential** time. Add pruning if possible.
- For shortest path in unweighted graphs, prefer **BFS**; use **IDDFS** only if memory is tight and small depth bound exists.

---

**End of notes.**
