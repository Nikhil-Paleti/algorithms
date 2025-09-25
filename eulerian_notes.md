# Eulerian Path and Circuit — Notes

## 1. Definitions

### Eulerian Path
An **Eulerian path** in a graph is a trail that **uses every edge exactly once**.  
- You may revisit nodes, but **each edge** must be traversed only once.  
- Start and end nodes can be different.  
- Exists in both directed and undirected graphs.

### Eulerian Circuit (Cycle)
An **Eulerian circuit** (or cycle) is a special Eulerian path that **starts and ends at the same node**.  
- Uses every edge exactly once.  
- Always a closed loop.

---

## 2. Conditions for Existence

### Undirected Graphs
- **Eulerian Circuit** exists if all vertices have **even degree** (every vertex has even number of edges).
- **Eulerian Path** exists if **0 or 2 vertices** have odd degree:
  - 0 odd-degree vertices → circuit exists.
  - 2 odd-degree vertices → open path exists (start at one odd, end at the other).

### Directed Graphs
- **Eulerian Circuit** exists if:
  - Graph is strongly connected.
  - Every vertex has **indegree = outdegree**.

- **Eulerian Path** exists if:
  - Graph is weakly connected.
  - Exactly one vertex has **outdegree = indegree + 1** (the start).
  - Exactly one vertex has **indegree = outdegree + 1** (the end).
  - All other vertices have **indegree = outdegree**.

---

## 3. Solving Eulerian Path / Circuit Problems

### Hierholzer’s Algorithm
Efficient algorithm (linear in edges) to find Eulerian paths/circuits:

1. Pick a starting node:
   - For Eulerian circuit: any node with edges.
   - For Eulerian path: the node with **outdegree = indegree + 1**.
2. Traverse edges:
   - While there are unused edges from current node, pick one (for lexicographic problems, pick smallest).
   - Remove (consume) that edge and move to the neighbor.
3. When a node has no more outgoing edges, append it to the route.
4. Reverse the route at the end.

**Key property:**  
- Each edge is used exactly once.  
- Appending on backtrack ensures edges are stitched into a valid Eulerian path.

### Complexity
- **Time:** \(O(E \log E)\) if using min-heaps for lexicographic order. Otherwise \(O(E)\).
- **Space:** \(O(V + E)\) for adjacency, route, and recursion.

---

## 4. Example: Reconstruct Itinerary (LeetCode 332)

**Problem:** Given tickets `[from, to]`, reconstruct an itinerary that uses all tickets once, starting from `"JFK"`, and is lexicographically smallest.

- Model: Directed multigraph (tickets = edges).
- Requirement: Use all tickets once ⇒ Eulerian path.
- Extra: Lexicographically smallest ⇒ choose smallest neighbor first.

**Solution:**
```python
from collections import defaultdict
from heapq import heappush, heappop

class Solution:
    def findItinerary(self, tickets):
        g = defaultdict(list)
        for u, v in tickets:
            heappush(g[u], v)

        route = []
        def dfs(u):
            while g[u]:
                v = heappop(g[u])
                dfs(v)
            route.append(u)

        dfs("JFK")
        return route[::-1]
```

---

## 5. Eulerian vs Hamiltonian

- **Eulerian Path:** Uses every **edge** exactly once. Nodes can repeat. Polynomial-time solvable.
- **Hamiltonian Path:** Visits every **node** exactly once. Edges can repeat. NP-complete problem.

---

## 6. Key Takeaways

- Eulerian problems are about **edges**, Hamiltonian problems are about **nodes**.
- Euler’s Theorem gives simple degree-based conditions for existence.
- **Hierholzer’s algorithm** is the go-to construction method.
- For interview problems (like Reconstruct Itinerary), remember:
  - Recognize it as Eulerian path.
  - Use DFS with min-heaps to ensure lexicographic order.
  - Append nodes on backtrack and reverse the result.
