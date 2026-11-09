import heapq

T = int(input())

for tc in range(T):
    N, O, M = map(int, input().split())
    digit = set(map(int, input().split()))
    operator = tuple(map(int, input().split()))
    W = int(input())

    INF = 10**18
    dist = [INF] * 1000

    origin = {}
    for i in range(1000):
        if set(map(int, str(i))) <= digit:
            origin[i] = len(str(i))
            dist[i] = len(str(i))

    pq = [(c, i) for i, c in origin.items()]
    heapq.heapify(pq)

    def helper(op, x, y):
        if op == 1: return x + y
        if op == 2: return x - y
        if op == 3: return x * y
        if op == 4: return x // y

    while pq:
        d, i = heapq.heappop(pq)
        if dist[i] < d: continue
        for op in operator:
            for ni, ni_cost in origin.items():
                if op == 4 and ni == 0: continue
                j = helper(op, i, ni)
                if 0 <= j <= 999:
                    nd = d + ni_cost + 1
                    if dist[j] > nd:
                        dist[j] = nd
                        heapq.heappush(pq, (nd, j))

    rst = dist[W] if W in origin else dist[W] + 1
    if rst > M or dist[W] >= INF:
        rst = -1
    print(f"#{tc+1} {rst}")