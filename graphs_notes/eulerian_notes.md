# Eulerian Path and Circuit — Notes

## 1. Definitions

### Eulerian Path
A path that **uses every edge exactly once**.  
- Vertices may repeat, but edges cannot.  
- The start and end vertices may differ.

### Eulerian Circuit (Cycle)
A special Eulerian path that **starts and ends at the same vertex**.  
- Uses every edge exactly once.  
- Always forms a closed loop.

---

## 2. Existence Conditions (Euler’s Theorem)

### Undirected Graphs
- **Eulerian Circuit**: All vertices have **even degree**.  
- **Eulerian Path**: Exactly **0 or 2 vertices** have odd degree.  
  - 0 odd-degree vertices → circuit exists.  
  - 2 odd-degree vertices → open path exists (must start at one odd-degree vertex and end at the other).

### Directed Graphs
- **Eulerian Circuit**:  
  - Graph is strongly connected.  
  - Every vertex has **indegree = outdegree**.  

- **Eulerian Path**:  
  - Graph is weakly connected.  
  - Exactly one vertex has **outdegree = indegree + 1** (the start).  
  - Exactly one vertex has **indegree = outdegree + 1** (the end).  
  - All other vertices: **indegree = outdegree**.

---

## 3. Algorithm to Construct Eulerian Path / Circuit

### Hierholzer’s Algorithm (General)
Efficient linear-time algorithm:

1. **Choose a start vertex**  
   - For Eulerian circuit: any vertex with edges.  
   - For Eulerian path: the unique vertex with `outdegree = indegree + 1` (or an odd-degree vertex in undirected case).  

2. **Walk edges until stuck**  
   - While the current vertex has unused edges, pick one, remove it, and continue.  
   - This produces a cycle (circuit) or partial path.

3. **Backtrack and stitch cycles**  
   - If you get stuck, add the vertex to the route.  
   - The recursion (or stack unwinding) will naturally stitch cycles into a valid path.

4. **Reverse the route** at the end (since vertices are added on backtrack).

### Complexity
- **Time:** O(E) for adjacency lists, or O(E log E) if edges must be chosen in order (e.g., lexicographically).  
- **Space:** O(V + E).

---

## 4. General Implementation (Undirected Graph)

```python
from collections import defaultdict

def find_eulerian_path(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)  # undirected graph

    route = []
    def dfs(u):
        while graph[u]:
            v = graph[u].pop()
            graph[v].remove(u)  # remove both directions
            dfs(v)
        route.append(u)

    dfs(edges[0][0])  # start from any vertex with edges
    return route[::-1]  # Eulerian path/circuit
```

---

## 5. Example: Directed Case (Itinerary / LC 332)

```python
from collections import defaultdict
from heapq import heappush, heappop

def eulerian_path_directed(tickets, start="JFK"):
    graph = defaultdict(list)
    for u, v in tickets:
        heappush(graph[u], v)  # maintain lexicographic order

    route = []
    def dfs(u):
        while graph[u]:
            v = heappop(graph[u])
            dfs(v)
        route.append(u)

    dfs(start)
    return route[::-1]
```

---

## 6. Eulerian vs Hamiltonian

- **Eulerian Path**: traverse every **edge** exactly once (vertices may repeat). Polynomial-time solvable with simple degree conditions.  
- **Hamiltonian Path**: visit every **vertex** exactly once (edges may repeat). **NP-complete**; no efficient general solution known.

---

## 7. Key Takeaways

- Eulerian = **edges**, Hamiltonian = **vertices**.  
- Degree conditions (Euler’s Theorem) let you decide existence in O(V+E).  
- **Hierholzer’s algorithm** builds the actual path in O(E).  
- Many interview/contest problems (like **Reconstruct Itinerary**) are Eulerian path problems with extra constraints (like lexicographic order).  
