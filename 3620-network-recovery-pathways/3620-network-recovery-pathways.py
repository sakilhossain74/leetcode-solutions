class Solution:
    def findMaxPathScore(self, edges: List[List[int]], online: List[bool], k: int) -> int:
        n = len(online)
        
        filtered = [(u, v, c) for u, v, c in edges if online[u] and online[v]]
        if not filtered:
            return -1
        
        adj = [[] for _ in range(n)]
        indeg = [0] * n
        for u, v, c in filtered:
            adj[u].append((v, c))
            indeg[v] += 1
        
        topo = []
        q = deque(i for i in range(n) if indeg[i] == 0)
        indeg_copy = indeg[:]
        while q:
            u = q.popleft()
            topo.append(u)
            for v, c in adj[u]:
                indeg_copy[v] -= 1
                if indeg_copy[v] == 0:
                    q.append(v)
        
        costs = sorted(set(c for _, _, c in filtered))
        
        def feasible(threshold: int) -> bool:
            dist = [float('inf')] * n
            dist[0] = 0
            for u in topo:
                if dist[u] == float('inf'):
                    continue
                for v, c in adj[u]:
                    if c >= threshold and dist[u] + c < dist[v]:
                        dist[v] = dist[u] + c
            return dist[n - 1] <= k
        
        lo, hi = 0, len(costs) - 1
        ans = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if feasible(costs[mid]):
                ans = costs[mid]
                lo = mid + 1
            else:
                hi = mid - 1
        
        return ans