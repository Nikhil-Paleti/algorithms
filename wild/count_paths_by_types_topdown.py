#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problem: Count type-covering paths in a road network
===================================================

You are given a set of shops connected by bidirectional roads. Each shop has a
**type** (e.g., grocery, sport, school, pharmacy). Multiple shops may share the
same type.

A **valid path** is a sequence of distinct shops such that:

1) The path visits **exactly one shop of each distinct type present in the input**.
2) Every pair of consecutive shops in the path is directly connected by a road.
3) The **order matters** — visiting the same set of shops in a different order
   counts as a different valid path.
4) There is **at most one road between any two shops**. Roads are bidirectional.

Return the **total number of valid paths**.

Input
-----
- `shop_types`: List[str] of length n, where `shop_types[i]` is the type of shop i.
- `roads`: List[List[int]] of undirected edges [u, v] with 0 <= u, v < n.

Output
------
- An integer: the number of valid paths that visit exactly one shop of each
  distinct type in any order using the given roads.

Constraints
-----------
- 1 ≤ n ≤ 50  (number of shops)
- 0 ≤ m ≤ 250 (number of roads)
- At most 1 road between two shops
- Roads are bidirectional

Notes
-----
- If there are T distinct types, each valid path has length T (number of nodes).
- Different orders count separately.
- Complexity of the provided solution is O((n + m) * 2^T) time (amortized via memoization)
  and O(n * 2^T) states.

Solution (Top-Down DP over subsets)
-----------------------------------
We use DFS with memoization. Map each distinct type to a bit [0..T-1].
A state is (node, mask), where `mask` is the set of types already used by the
partial path and `node` is the current endpoint. From (node, mask), we can move
to any neighbor `v` whose type `t(v)` is not yet in `mask`, adding it to the
mask. When mask == (1<<T) - 1, we've used exactly one shop for every type, so
we count 1.

This counts each order separately because the DFS explores different sequences.
"""

from functools import lru_cache
from collections import defaultdict
from typing import List, Tuple


def count_valid_paths_topdown(shop_types: List[str], roads: List[Tuple[int, int]]) -> int:
    """
    Count all valid paths that visit exactly one shop of each distinct type.

    Args:
        shop_types: list of shop type strings of length n.
        roads: list of undirected edges (u, v).

    Returns:
        Total number of valid paths.
    """
    n = len(shop_types)
    if n == 0:
        return 0

    # Build graph (adjacency list)
    graph = [[] for _ in range(n)]
    for u, v in roads:
        if u == v:
            # ignore self-loops; they can't help build length-T paths with distinct nodes
            continue
        graph[u].append(v)
        graph[v].append(u)

    # Map each distinct type to a bit position
    # (preserve order of first appearance for determinism)
    distinct_types = list(dict.fromkeys(shop_types))
    T = len(distinct_types)
    tbit = {t: i for i, t in enumerate(distinct_types)}
    full_mask = (1 << T) - 1

    # Precompute type bit for each node
    node_tbit = [tbit[tp] for tp in shop_types]

    @lru_cache(maxsize=None)
    def dfs(node: int, mask: int) -> int:
        """
        Number of paths ending at `node` having already used the set of types in `mask`.
        """
        if mask == full_mask:
            # All types used exactly once
            return 1

        total = 0
        for nei in graph[node]:
            tb = node_tbit[nei]
            if (mask >> tb) & 1:
                # This neighbor's type already used — can't include another shop of same type
                continue
            total += dfs(nei, mask | (1 << tb))
        return total

    # Start from every node as a length-1 path using its own type.
    ans = 0
    for u in range(n):
        start_mask = 1 << node_tbit[u]
        ans += dfs(u, start_mask)

    return ans


# --------------------------
# Example usage & quick tests
# --------------------------
if __name__ == "__main__":
    # Example 1
    shop_types = ["grocery", "sport", "school", "pharmacy"]
    roads = [(0, 1), (1, 2), (2, 3), (0, 3)]
    print("Example 1:", count_valid_paths_topdown(shop_types, roads))

    # Example 2: two shops share a type; only one per type allowed
    shop_types2 = ["A", "B", "A"]
    roads2 = [(0, 1), (1, 2), (0, 2)]
    # Distinct types = {A, B} -> T=2; valid paths are A->B and B->A if edges exist
    print("Example 2:", count_valid_paths_topdown(shop_types2, roads2))

    # Example 3: disconnected graph -> might yield zero
    shop_types3 = ["x", "y", "z"]
    roads3 = [(0, 1)]  # no road to 2 -> no path that uses all three
    print("Example 3:", count_valid_paths_topdown(shop_types3, roads3))
