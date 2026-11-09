import heapq

T = int(input())

for tc in range(T):
    N, O, M = map(int, input().split())
    digit = set(map(int, input().split()))
    operator = tuple(map(int, input().split()))
    W = int(input())

    pq = []
    INF = 10**18
    dist = [ INF for _ in range(1000) ]
    origin = set()
    for i in range(1000):
        if set(digit) >= set(map(int, str(i))):
            dist[i] = len(str(i))
            origin.add(i)
            heapq.heappush(pq, (dist[i], i))

    def helper(op, x, y):
        if op == 1: return x+y
        if op == 2: return x-y
        if op == 3: return x*y
        if op == 4: return x//y

    while pq:
        d, i = heapq.heappop(pq)
        if dist[i] < d: continue

        for op in operator:
            for ni in range(1000):
                if not(op == 4 and ni == 0):
                    j = helper(op, i, ni)
                    if j < 0 or j > 999:
                        continue
                    if dist[j] > dist[i] + dist[ni] + 1:
                        dist[j] = dist[i] + dist[ni] + 1
                        heapq.heappush(pq, (dist[j], j))

                if not(op == 4 and i == 0):
                    j = helper(op, ni, i)
                    if j < 0 or j > 999:
                        continue
                    if dist[j] > dist[i] + dist[ni] + 1:
                        dist[j] = dist[i] + dist[ni] + 1
                        heapq.heappush(pq, (dist[j], j))

    rst = dist[W] if W in origin else dist[W]+1
    if rst > M: rst = -1
    print(f"#{tc+1} {rst}")

    # print('dist:', *range(100), sep='\t')
    # for i in range(0, 1000, 100):
    #     print(i, ':', *[j if j < 10**18 else -1 for j in dist[i:i+100]], sep='\t')
    # print()