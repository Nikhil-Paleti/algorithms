# BFS Variants — Notes (with LeetCode examples + Complexity)

BFS explores graphs level by level. Below, each variant includes a representative LeetCode problem, Python solution, and complexity analysis.

---

## 1) Standard BFS
**LeetCode 752 — Open the Lock**  

- **Time:** O(V + E), where V = 10^4 possible states, E = 8*V edges.  
- **Space:** O(V).

```python
# LC 752: Open the Lock
from typing import List
from collections import deque

class Solution:
    def openLock(self, deadends: List[str], target: str) -> int:
        dead = set(deadends)
        if "0000" in dead:
            return -1
        if target == "0000":
            return 0

        def neighbors(state: str):
            s = list(state)
            for i in range(4):
                d = int(s[i])
                for nd in ((d + 1) % 10, (d - 1) % 10):
                    s[i] = str(nd)
                    yield "".join(s)
                s[i] = str(d)

        q = deque([("0000", 0)])
        seen = {"0000"}
        while q:
            u, dist = q.popleft()
            for v in neighbors(u):
                if v in dead or v in seen:
                    continue
                if v == target:
                    return dist + 1
                seen.add(v)
                q.append((v, dist + 1))
        return -1
```

---

## 2) Multi-Source BFS
**LeetCode 994 — Rotting Oranges**  

- **Time:** O(mn).  
- **Space:** O(mn).

```python
# LC 994: Rotting Oranges
from typing import List
from collections import deque

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        q = deque()
        fresh = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 2:
                    q.append((r, c, 0))
                elif grid[r][c] == 1:
                    fresh += 1

        time = 0
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        while q:
            r, c, t = q.popleft()
            time = max(time, t)
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc, t + 1))

        return time if fresh == 0 else -1
```

---

## 3) 0–1 BFS (Deque)
**LeetCode 1368 — Minimum Cost to Make at Least One Valid Path in a Grid**  

- **Time:** O(mn).  
- **Space:** O(mn).

```python
# LC 1368: Minimum Cost to Make at Least One Valid Path in a Grid
from typing import List
from collections import deque

class Solution:
    def minCost(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dirs = [(0,0),(0,1),(0,-1),(1,0),(-1,0)]
        INF = 10**9
        dist = [[INF]*n for _ in range(m)]
        dist[0][0] = 0
        dq = deque([(0, 0)])

        while dq:
            r, c = dq.popleft()
            for d in range(1,5):
                nr, nc = r + dirs[d][0], c + dirs[d][1]
                if 0 <= nr < m and 0 <= nc < n:
                    w = 0 if d == grid[r][c] else 1
                    if dist[nr][nc] > dist[r][c] + w:
                        dist[nr][nc] = dist[r][c] + w
                        if w == 0:
                            dq.appendleft((nr, nc))
                        else:
                            dq.append((nr, nc))
        return dist[m-1][n-1]
```

---

## 4) Weighted BFS Variants

### A) BFS with Priority Queue (Dijkstra)
**LeetCode 743 — Network Delay Time**  

- **Time:** O(E log V).  
- **Space:** O(V + E).

```python
# LC 743: Network Delay Time (Dijkstra)
from typing import List
import heapq

class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        g = [[] for _ in range(n+1)]
        for u, v, w in times:
            g[u].append((v, w))

        dist = [float('inf')] * (n+1)
        dist[k] = 0
        pq = [(0, k)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in g[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))

        ans = max(dist[1:])
        return -1 if ans == float('inf') else ans
```

### B) Dial’s Algorithm  
- **Time:** O(V + E).  
- **Space:** O(V + E).

---

## 5) BFS on Grids
**LeetCode 1091 — Shortest Path in Binary Matrix**  

- **Time:** O(n^2).  
- **Space:** O(n^2).

```python
# LC 1091: Shortest Path in Binary Matrix
from typing import List
from collections import deque

class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if grid[0][0] or grid[n-1][n-1]:
            return -1
        q = deque([(0, 0, 1)])
        grid[0][0] = 1
        dirs = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        while q:
            r, c, d = q.popleft()
            if r == n-1 and c == n-1:
                return d
            for dr, dc in dirs:
                nr, nc = r+dr, c+dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    grid[nr][nc] = 1
                    q.append((nr, nc, d+1))
        return -1
```

---

## 6) Bipartite Graph Check BFS
**LeetCode 785 — Is Graph Bipartite?**  

- **Time:** O(V + E).  
- **Space:** O(V).

```python
# LC 785: Is Graph Bipartite?
from typing import List
from collections import deque

class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        n = len(graph)
        color = [0]*n

        for i in range(n):
            if color[i] != 0:
                continue
            color[i] = 1
            q = deque([i])
            while q:
                u = q.popleft()
                for v in graph[u]:
                    if color[v] == 0:
                        color[v] = -color[u]
                        q.append(v)
                    elif color[v] == color[u]:
                        return False
        return True
```

---

## 7) BFS for Topological Sort (Kahn’s Algorithm)
**LeetCode 210 — Course Schedule II**  

- **Time:** O(V + E).  
- **Space:** O(V + E).

```python
# LC 210: Course Schedule II (Kahn's Algorithm)
from typing import List
from collections import deque

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        g = [[] for _ in range(numCourses)]
        indeg = [0]*numCourses
        for c, pre in prerequisites:
            g[pre].append(c)
            indeg[c] += 1

        q = deque([i for i in range(numCourses) if indeg[i] == 0])
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in g[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)

        return order if len(order) == numCourses else []
```

---

## 8) BFS with State Encoding
**LeetCode 1293 — Shortest Path in a Grid with Obstacles Elimination**  

- **Time:** O(mn * k).  
- **Space:** O(mn * k).

```python
# LC 1293: Shortest Path in a Grid with Obstacles Elimination
from typing import List
from collections import deque

class Solution:
    def shortestPath(self, grid: List[List[int]], k: int) -> int:
        m, n = len(grid), len(grid[0])
        if k >= m + n - 2:
            return m + n - 2

        best = [[-1]*n for _ in range(m)]
        best[0][0] = k

        q = deque([(0, 0, k, 0)])
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        while q:
            r, c, rem, d = q.popleft()
            if r == m-1 and c == n-1:
                return d
            for dr, dc in dirs:
                nr, nc = r+dr, c+dc
                if 0 <= nr < m and 0 <= nc < n:
                    nrem = rem - grid[nr][nc]
                    if nrem >= 0 and nrem > best[nr][nc]:
                        best[nr][nc] = nrem
                        q.append((nr, nc, nrem, d+1))
        return -1
```

---

## 9) Bidirectional BFS
**LeetCode 127 — Word Ladder**  

- **Time:** O(L * N), where L = word length, N = number of words.  
- **Space:** O(N).

```python
# LC 127: Word Ladder (Bidirectional BFS)
from typing import List
from collections import defaultdict

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        wordSet = set(wordList)
        if endWord not in wordSet:
            return 0

        buckets = defaultdict(list)
        L = len(beginWord)
        for w in wordSet | {beginWord}:
            for i in range(L):
                buckets[w[:i] + "*" + w[i+1:]].append(w)

        begin = {beginWord}
        end = {endWord}
        visited = {beginWord, endWord}
        steps = 1

        def expand(frontier: set) -> set:
            nxt = set()
            for w in frontier:
                for i in range(L):
                    pattern = w[:i] + "*" + w[i+1:]
                    for nei in buckets[pattern]:
                        if nei not in visited:
                            visited.add(nei)
                            nxt.add(nei)
            return nxt

        while begin and end:
            if len(begin) > len(end):
                begin, end = end, begin
            begin = expand(begin)
            steps += 1
            if begin & end:
                return steps
        return 0
```

---

## 🔑 Key Takeaways
- **Standard BFS:** O(V+E).  
- **Multi-source BFS:** O(V+E).  
- **0–1 BFS:** O(V+E).  
- **Weighted BFS:** O(E log V) or O(V+E) with Dial’s.  
- **Grid BFS:** O(n^2).  
- **Bipartite BFS:** O(V+E).  
- **Topological BFS:** O(V+E).  
- **Stateful BFS:** O(V * states).  
- **Bidirectional BFS:** O(b^(d/2)), faster in practice.
