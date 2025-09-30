# Graph Algorithms — New Grad Interview Notes

This file summarizes the **core graph algorithms** you should know for interviews, plus a few **bonus algorithms** worth learning later.

---

## ✅ Core Algorithms (Must-Know)

### 1. DFS (Depth-First Search)
- **Purpose:** Graph traversal, pathfinding, connected components, cycle detection.  
- **Complexity:** O(V + E).  
- **Notes:**  
  - Recursive or stack-based.  
  - Useful for detecting back edges (cycle detection in directed graphs).  

### 2. BFS (Breadth-First Search)
- **Purpose:** Shortest path in **unweighted** graphs, level-order traversal.  
- **Complexity:** O(V + E).  
- **Notes:**  
  - Uses a queue.  
  - Great for shortest path problems where edge weights = 1.  

### 3. Topological Sort
- **Purpose:** Order vertices in a DAG such that all edges go forward.  
- **Complexity:** O(V + E).  
- **Notes:**  
  - Implement via DFS (postorder) or BFS (Kahn’s algorithm).  
  - Detects cycles (if topological order is impossible).  
  - Used in scheduling and dependency problems.  

### 4. Union–Find (Disjoint Set Union, DSU)
- **Purpose:** Track connected components, cycle detection, Kruskal’s MST.  
- **Complexity:** ~O(α(V)) per operation (inverse Ackermann, almost constant).  
- **Notes:**  
  - Supports union by rank + path compression.  
  - Core building block for Kruskal’s.  

### 5. Dijkstra’s Algorithm
- **Purpose:** Single-source shortest paths in weighted graphs (non-negative weights).  
- **Complexity:** O((V + E) log V) with heap.  
- **Notes:**  
  - Greedy algorithm.  
  - Cannot handle negative weights.  

### 6. Bellman–Ford Algorithm
- **Purpose:** Single-source shortest paths with **negative weights**, detect negative cycles.  
- **Complexity:** O(V * E).  
- **Notes:**  
  - Dynamic programming style.  
  - Works even when negative edges exist.  

### 7. Floyd–Warshall Algorithm
- **Purpose:** All-pairs shortest paths.  
- **Complexity:** O(V³).  
- **Notes:**  
  - DP-based algorithm.  
  - Handles negative edges but not negative cycles.  

### 8. Prim’s Algorithm
- **Purpose:** Minimum Spanning Tree (MST).  
- **Complexity:** O(E log V) with heap.  
- **Notes:**  
  - Greedy: expand MST from a seed node.  

### 9. Kruskal’s Algorithm
- **Purpose:** Minimum Spanning Tree (MST).  
- **Complexity:** O(E log V).  
- **Notes:**  
  - Sort edges, use Union–Find to add safe edges.  
  - Simpler to code than Prim’s.  

### 10. Eulerian Path and Circuit
- **Purpose:** Path/circuit that uses every edge exactly once.  
- **Conditions:**  
  - Undirected:  
    - Circuit → all vertices have even degree.  
    - Path → exactly 0 or 2 vertices of odd degree.  
  - Directed:  
    - Circuit → indegree = outdegree for all vertices.  
    - Path → one node with outdegree = indegree + 1, one with indegree = outdegree + 1, rest equal.  
- **Algorithm:** Hierholzer’s Algorithm (O(E)).  
- **Notes:**  
  - Used in “Reconstruct Itinerary” type problems.  

### 11. Cycle Detection
- **Undirected Graphs:**  
  - Use Union–Find or DFS (check back edges).  
- **Directed Graphs:**  
  - Use DFS with recursion stack (detect back edges).  
- **Complexity:** O(V + E).  

---

## ⚡ High ROI Additions (Good Next Step)

### 12. Strongly Connected Components (SCCs)
- **Algorithms:** Kosaraju’s or Tarjan’s.  
- **Purpose:** Decompose directed graphs into SCCs.  
- **Applications:** 2-SAT, condensation graphs, dependency analysis.  

### 13. Bipartite Graph Check
- **Purpose:** Check if graph is 2-colorable.  
- **Method:** BFS/DFS with alternate coloring.  
- **Applications:** Matching problems, cycle parity detection.  

### 14. DAG Shortest Path
- **Purpose:** Fast shortest paths in DAGs.  
- **Method:** Topological sort + relaxation.  
- **Complexity:** O(V + E).  

---

## 🎯 Bonus / Advanced (Not core for new grads, but useful later)

- **Max Flow / Min Cut (Ford–Fulkerson, Edmonds–Karp, Dinic’s)**  
  - Applications: network flow, bipartite matching.  

- **Articulation Points and Bridges**  
  - DFS-based (Tarjan’s algorithm).  
  - Applications: network reliability, critical connections.  

- **Lowest Common Ancestor (LCA)**  
  - Applications: tree queries.  
  - Implement with Binary Lifting or Euler Tour + RMQ.  

---

## 🔑 Key Takeaways
- **DFS/BFS** are foundations for almost everything.  
- **Dijkstra, Bellman–Ford, Floyd** cover shortest path variants.  
- **Prim + Kruskal** for MST.  
- **Union–Find, Topological Sort, Cycle Detection** are core utilities.  
- **Eulerian paths** are edge-based traversal problems.  
- Once comfortable, add **SCC, Bipartite check, DAG shortest path** for extra depth.  
