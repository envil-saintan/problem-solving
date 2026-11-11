T = int(input())

for tc in range(1, T+1):
    N = int(input())
    grid = [ input().split() for _ in range(N) ]

    for y in range(N):
        for x in range(N):
            if grid[y][x] in "12":
                grid[y][x] = 1
            elif grid[y][x] in "3456":
                grid[y][x] = 2
            else:
                grid[y][x] = 0

    # print(grid)
    # 우리가 뭘할꺼냐면...

    

    from collections import deque
    q = deque() # (r, c, x)가 이제 들어가는 거예요

    # 이제 좀 방향을 구체적으로 정해두고 시작합시다
    dy = ( 0, 1, 0, -1 )
    dx = ( 1, 0, -1, 0 )
    # [0]오른쪽, [1]아래, [2]왼쪽, [3]위 순서예요

    # 1번 타입
    # 확실하게 갑시다
    # type1[?][0]에서 들어와서, type1[?][1]로 나간다
    type1 = [ (0, 2), (1, 3), (2, 0), (3, 1) ]

    # 2번 타입일 때 그럼...
    # 귀찮으니 생략하겠습니다
    # [0]은 오른쪽이랑 아래를 잇는거겠네요
    type2 = [ (0, 1), (1, 2), (2, 3), (3, 0),
              (1, 0), (2, 1), (3, 2), (0, 3) ]

    INF = 10**18
    dist = [ [ [INF]*8 for x in range(N) ] for y in range(N) ]
    # dist[y][x][k] := (y, x)에 있는 파이프가 k번 타입이라고 했을 때, 
    # 여기까지 도달하는 최단거리

    # 첫 시작점은 항상 왼쪽과 이어져 있어야 합니다
    # 그러므로... 1번 타입이라면 좌우 연결인 머시기겠다 그죠?
    # 그게 0번, 2번.
    if grid[0][0] == 1:
        dist[0][0][2] = 1 # 1번 타입의 2번째 모양, 왼쪽에서 들어와서 오른쪽으로 나가는 것만
        q.append( (0, 0, 2) )

    # 2번 타입이라면...?
    # 왼쪽과 위를 연결한 것, 왼쪽과 아래를 연결한 것, 두 종류네요.
    # (사실 왼쪽과 아래를 연결한 것만 인정되긴 할 겁니다. 위로 가면 벽인걸요)
    if grid[0][0] == 2:
        dist[0][0][5] = 1 # 2번 타입의 5번째 모양, 왼쪽에서 들어와서 아래로 나가는 것만
        q.append( (0, 0, 5) )

    # 이제 BFS 시작입니다
    while q: # 큐에 뭔가 남아 있는 동안
        r, c, x = q.popleft()

        # 나가는 칸 보기!
        # 이거 1번 타입이라면!
        nr, nc, 나가는방향 = -1, -1, -1
        if grid[r][c] == 1:
            # 현재 칸 기준 나가는 방향은 이거
            나가는방향 = type1[x][1]
            nr = r + dy[나가는방향]
            nc = c + dx[나가는방향]
            # 얘가 나가는 방향에 있는 칸을 가져왔네요!
        elif grid[r][c] == 2:
            나가는방향 = type2[x][1]
            nr = r + dy[나가는방향]
            nc = c + dx[나가는방향]

        # 그럼 이제 다음 칸인 (nr, nc)에서
        # 얘가 1번 타입의 파이프냐, 2번 타입의 파이프냐도 고려해야 합니다.
        # 다만 그 이전에... 
        # 이게 valid한 좌표인지도 파악해야 겠네요.
        if nr < 0 or nc < 0 or nr >= N or nc >= N:
            continue

        들어오는방향 = (나가는방향 + 2) % 4
        if grid[nr][nc] == 1:
            # 모든 이 타입에 대해서 저 방향으로 시작하는 것을 걸러낼 수 있다는 말이긴 한데요
            # 코드로 보는 게 더 이해빠르실듯
            for k in range(len(type1)):
                i, o = type1[k]
                if i == 들어오는방향:
                    # 그럼 얘는 쓸 수 있다는 뜻!
                    # 다만... 이미 INF가 아닌 값이라거나 할 수도 있긴 한데요
                    # 그러므로 더 나쁜 값으로 덮어쓰면 안 됩니다
                    if dist[nr][nc][k] > dist[r][c][x] + 1:
                        dist[nr][nc][k] = dist[r][c][x] + 1
                        q.append( (nr, nc, k) )
        if grid[nr][nc] == 2:
            for k in range(len(type2)):
                i, o = type2[k]
                if i == 들어오는방향:
                    if dist[nr][nc][k] > dist[r][c][k] + 1:
                        dist[nr][nc][k] = dist[r][c][k] + 1
                        q.append( (nr, nc, k) )

    # 이제 저 while문이 끝난다면
    # 아무튼 각 칸 및 각 상태에 대해서 최단 거리가 구해진 상태일 겁니다
    # dist배열에 잘 저장되어 있겠죠

    # 이제 우리가 관심이 있는 값은,
    # dist[N-1][N-1][?]
    # 여기입니다.

    # 다만 모든 값이 아니라...
    # 오른쪽으로 나가는 방향에 있는 값을 생각해야 합니다.
    # 그러므로

    ans = INF
    if grid[N-1][N-1] == 1:
        for k in range( len(type1) ):
            i, o = type1[k]
            if o == 0: # 오른쪽으로 나가는 머시기
                ans = min(ans, dist[N-1][N-1][k])

    if grid[N-1][N-1] == 2:
        for k in range( len(type2) ):
            i, o = type2[k]
            if o == 0:
                ans = min(ans, dist[N-1][N-1][k])

    print(f"#{tc} {ans}")