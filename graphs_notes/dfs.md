# DFS Variants — Notes (with LeetCode examples + Complexity)

DFS (Depth-First Search) comes in many flavors. For each variant below, you’ll find a representative LeetCode problem, a clean Python solution, and a brief complexity analysis.

---

## 1) Based on *What* You Traverse

### A. Node Traversal (Vertex-DFS)
**LeetCode 547 — Number of Provinces**  
Visit each node once to count connected components in an undirected graph.

- **Time:** O(n²) because the graph is given as an n×n adjacency matrix.  
- **Space:** O(n) for `seen` and recursion stack.

```python
# LC 547: Number of Provinces
from typing import List

class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        seen = [False]*n

        def dfs(u: int) -> None:
            seen[u] = True
            for v in range(n):
                if isConnected[u][v] and not seen[v]:
                    dfs(v)

        count = 0
        for i in range(n):
            if not seen[i]:
                count += 1
                dfs(i)
        return count
```

### B. Path Traversal (Edge/Path DFS — enumerate paths)
**LeetCode 797 — All Paths From Source to Target**  
Explore *paths* (backtracking) from node `0` to node `n-1`.

- **Time:** O(#paths + V + E) → worst-case exponential in V.  
- **Space:** O(V) recursion depth + O(V) path buffer (excludes output).

```python
# LC 797: All Paths From Source to Target
from typing import List

class Solution:
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        n = len(graph)
        path, ans = [0], []

        def dfs(u: int):
            if u == n - 1:
                ans.append(path.copy())
                return
            for v in graph[u]:
                path.append(v)
                dfs(v)
                path.pop()

        dfs(0)
        return ans
```

---

## 2) Based on *How* You Implement

### A. Recursive DFS
**LeetCode 695 — Max Area of Island**

- **Time:** O(mn) — each cell visited at most once.  
- **Space:** O(mn) worst-case recursion (island covering grid).

```python
# LC 695: Max Area of Island
from typing import List

class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        def dfs(r, c) -> int:
            if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] == 0:
                return 0
            grid[r][c] = 0
            area = 1
            area += dfs(r+1, c) + dfs(r-1, c) + dfs(r, c+1) + dfs(r, c-1)
            return area

        best = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    best = max(best, dfs(i, j))
        return best
```

### B. Iterative DFS (Explicit Stack)
**LeetCode 200 — Number of Islands** (stack version)

- **Time:** O(mn).  
- **Space:** O(mn) in worst case for the stack/visited marks.

```python
# LC 200: Number of Islands (iterative DFS)
from typing import List

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        m, n = len(grid), len(grid[0])
        ans = 0

        for i in range(m):
            for j in range(n):
                if grid[i][j] == '1':
                    ans += 1
                    stack = [(i, j)]
                    grid[i][j] = '0'
                    while stack:
                        r, c = stack.pop()
                        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                            nr, nc = r+dr, c+dc
                            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == '1':
                                grid[nr][nc] = '0'
                                stack.append((nr, nc))
        return ans
```

---

## 3) Based on *Coloring / States*

### A. 3-Color DFS (White-Gray-Black) — Cycle Detection
**LeetCode 207 — Course Schedule**

- **Time:** O(V + E).  
- **Space:** O(V + E) for graph + O(V) recursion stack.

```python
# LC 207: Course Schedule
from typing import List

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        adj = [[] for _ in range(numCourses)]
        for c, pre in prerequisites:
            adj[pre].append(c)

        color = [0]*numCourses  # 0=white, 1=gray, 2=black

        def dfs(u: int) -> bool:
            color[u] = 1
            for v in adj[u]:
                if color[v] == 1:
                    return False    # back edge -> cycle
                if color[v] == 0 and not dfs(v):
                    return False
            color[u] = 2
            return True

        for i in range(numCourses):
            if color[i] == 0 and not dfs(i):
                return False
        return True
```

### B. Timestamp DFS (Discovery/Finish Times)
**LeetCode 2360 — Longest Cycle in a Graph**  
Use a `time`/step map to measure cycle length when revisiting a node in the same walk.

- **Time:** O(n) — each node processed once.  
- **Space:** O(n) for `seen` and local hash map per component.

```python
# LC 2360: Longest Cycle in a Graph
from typing import List

class Solution:
    def longestCycle(self, edges: List[int]) -> int:
        n = len(edges)
        seen = [False]*n
        ans = -1

        for i in range(n):
            if seen[i]: 
                continue
            t = {}
            u = i
            step = 0
            while u != -1 and not seen[u]:
                if u in t:
                    ans = max(ans, step - t[u])
                    break
                t[u] = step
                step += 1
                seen[u] = True
                u = edges[u]
        return ans
```

---

## 4) Special Variants

### A. Backtracking DFS
**LeetCode 51 — N-Queens**

- **Time:** O(N!) in the classic analysis (pruned).  
- **Space:** O(N) recursion + O(N) sets; output not counted.

```python
# LC 51: N-Queens (backtracking)
from typing import List

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        cols = set()
        diag1 = set()  # r-c
        diag2 = set()  # r+c
        board = [['.']*n for _ in range(n)]
        ans = []

        def dfs(r: int):
            if r == n:
                ans.append([''.join(row) for row in board])
                return
            for c in range(n):
                if c in cols or (r-c) in diag1 or (r+c) in diag2:
                    continue
                cols.add(c); diag1.add(r-c); diag2.add(r+c)
                board[r][c] = 'Q'
                dfs(r+1)
                board[r][c] = '.'
                cols.remove(c); diag1.remove(r-c); diag2.remove(r+c)

        dfs(0)
        return ans
```

### B. Topological DFS (Postorder)
**LeetCode 210 — Course Schedule II**

- **Time:** O(V + E).  
- **Space:** O(V + E) for graph + O(V) recursion + O(V) output list.

```python
# LC 210: Course Schedule II (Topo via DFS postorder)
from typing import List

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        adj = [[] for _ in range(numCourses)]
        for c, pre in prerequisites:
            adj[pre].append(c)

        color = [0]*numCourses  # 0=white,1=gray,2=black
        order = []
        ok = True

        def dfs(u: int):
            nonlocal ok
            color[u] = 1
            for v in adj[u]:
                if color[v] == 1:
                    ok = False
                    return
                if color[v] == 0:
                    dfs(v)
                    if not ok: 
                        return
            color[u] = 2
            order.append(u)

        for i in range(numCourses):
            if color[i] == 0:
                dfs(i)
                if not ok: 
                    return []
        return order[::-1]
```

### C. DFS Tree Edge Classification (tree/back/forward/cross)
**LeetCode 802 — Find Eventual Safe States**  
Nodes with *no* path to a cycle are safe. Back edges imply cycles.

- **Time:** O(V + E).  
- **Space:** O(V) for colors/safe + recursion.

```python
# LC 802: Find Eventual Safe States
from typing import List

class Solution:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        n = len(graph)
        color = [0]*n  # 0=white,1=gray,2=black
        safe = [False]*n

        def dfs(u: int) -> bool:
            color[u] = 1
            for v in graph[u]:
                if color[v] == 1:     # back edge -> cycle
                    return False
                if color[v] == 0 and not dfs(v):
                    return False
            color[u] = 2
            safe[u] = True
            return True

        for i in range(n):
            if color[i] == 0:
                dfs(i)
        return [i for i in range(n) if safe[i]]
```

### D. Low-Link DFS (Tarjan) — Bridges / Articulation / SCC
**LeetCode 1192 — Critical Connections in a Network** (bridges)

- **Time:** O(V + E).  
- **Space:** O(V + E) for graph + arrays + recursion.

```python
# LC 1192: Critical Connections in a Network (bridges via Tarjan)
from typing import List

class Solution:
    def criticalConnections(self, n: int, connections: List[List[int]]) -> List[List[int]]:
        adj = [[] for _ in range(n)]
        for a, b in connections:
            adj[a].append(b)
            adj[b].append(a)

        time = 0
        disc = [-1]*n
        low  = [-1]*n
        ans = []

        def dfs(u: int, parent: int):
            nonlocal time
            disc[u] = low[u] = time
            time += 1
            for v in adj[u]:
                if v == parent:
                    continue
                if disc[v] == -1:
                    dfs(v, u)
                    low[u] = min(low[u], low[v])
                    if low[v] > disc[u]:
                        ans.append([u, v])  # bridge
                else:
                    low[u] = min(low[u], disc[v])

        for i in range(n):
            if disc[i] == -1:
                dfs(i, -1)
        return ans
```

### E. Euler Tour DFS (Flatten subtree intervals)
**LeetCode 1519 — Number of Nodes in the Sub-Tree With the Same Label**  
We record Euler `tin/tout` as an optional technique to reason about subtrees.

- **Time:** O(n + 26·n) ≈ O(n).  
- **Space:** O(n) for graph/visited + recursion; O(26) per stack frame.

```python
# LC 1519: Number of Nodes in the Sub-Tree With the Same Label
from typing import List
from collections import defaultdict

class Solution:
    def countSubTrees(self, n: int, edges: List[List[int]], labels: str) -> List[int]:
        g = [[] for _ in range(n)]
        for a, b in edges:
            g[a].append(b)
            g[b].append(a)

        ans = [0]*n
        seen = [False]*n

        def dfs(u: int) -> List[int]:
            seen[u] = True
            freq = [0]*26
            idx = ord(labels[u]) - 65 if 'A' <= labels[u] <= 'Z' else ord(labels[u]) - 97
            freq[idx] += 1
            for v in g[u]:
                if not seen[v]:
                    child = dfs(v)
                    for i in range(26):
                        freq[i] += child[i]
            ans[u] = freq[idx]
            return freq

        dfs(0)
        return ans
```

### F. Lexicographic DFS
**LeetCode 332 — Reconstruct Itinerary**  
DFS (Hierholzer) using min-heap or sorted order to get lexicographically smallest itinerary.

- **Time:** O(E log E) due to heap pushes/pops across all edges.  
- **Space:** O(E) for graph + O(E) route stack.

```python
# LC 332: Reconstruct Itinerary (DFS + lexicographic order)
from typing import List
from collections import defaultdict
import heapq

class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        g = defaultdict(list)
        for a, b in tickets:
            heapq.heappush(g[a], b)  # min-heap for lexicographic order

        route = []
        def dfs(u: str):
            while g[u]:
                v = heapq.heappop(g[u])
                dfs(v)
            route.append(u)

        dfs("JFK")
        return route[::-1]
```

---

## 5) Hybrid / Application-Oriented

### A. Iterative Deepening DFS (IDDFS)
**LeetCode 1971 — Find if Path Exists in Graph**  
(Usually plain DFS/BFS; here shown with depth-limits to illustrate IDDFS.)

- **Time:** O(D·(V + E)) where D is depth limit tried (amortizes to O(V+E) on trees).  
- **Space:** O(V) for visited/stack in each depth-limited search.

```python
# LC 1971: Find if Path Exists in Graph (IDDFS illustration)
from typing import List

class Solution:
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        g = [[] for _ in range(n)]
        for a, b in edges:
            g[a].append(b)
            g[b].append(a)

        if source == destination:
            return True

        def dls(limit: int) -> bool:
            seen = [False]*n
            stack = [(source, 0)]
            seen[source] = True
            while stack:
                u, d = stack.pop()
                if u == destination:
                    return True
                if d == limit:
                    continue
                for v in g[u]:
                    if not seen[v]:
                        seen[v] = True
                        stack.append((v, d+1))
            return False

        # Increase depth limit until found or all nodes depth covered
        for L in range(n):  # worst-case depth < n
            if dls(L):
                return True
        return False
```

### B. Randomized DFS
**LeetCode 133 — Clone Graph** (order doesn’t matter; randomizing neighbor order illustrates randomized DFS)

- **Time:** O(V + E).  
- **Space:** O(V + E) for map and cloned graph.

```python
# LC 133: Clone Graph (randomized neighbor order demonstration)
from typing import Optional
import random

# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

class Solution:
    def cloneGraph(self, node: 'Optional[Node]') -> 'Optional[Node]':
        if not node:
            return None
        mp = {}

        def dfs(u: 'Node') -> 'Node':
            if u in mp:
                return mp[u]
            copy = Node(u.val)
            mp[u] = copy
            nbrs = list(u.neighbors)
            random.shuffle(nbrs)  # randomized DFS order
            for v in nbrs:
                copy.neighbors.append(dfs(v))
            return copy

        return dfs(node)
```

### C. DFS with Memoization (DP on Graphs)
**LeetCode 329 — Longest Increasing Path in a Matrix**

- **Time:** O(mn) — each cell memoized and expanded to 4 neighbors once.  
- **Space:** O(mn) for memo + O(mn) worst-case recursion.

```python
# LC 329: Longest Increasing Path in a Matrix (DFS + memo)
from typing import List
from functools import lru_cache

class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        m, n = len(matrix), len(matrix[0])

        @lru_cache(None)
        def dfs(r: int, c: int) -> int:
            best = 1
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr, nc = r+dr, c+dc
                if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:
                    best = max(best, 1 + dfs(nr, nc))
            return best

        return max(dfs(i, j) for i in range(m) for j in range(n))
```

---

## 🔑 Key Takeaways
- **Traversal flavor** → Node vs Path.  
- **Implementation flavor** → Recursive vs Stack.  
- **State tracking** → Colors, timestamps, low-link values.  
- **Applications** → Cycle detection, SCCs/bridges, Euler tours, backtracking, memoized DP, IDDFS, randomized DFS.
