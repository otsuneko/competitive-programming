import heapq  # heapqライブラリのimport

Q = int(input())
balls = []
add = 0
for i in range(Q):
    query = list(map(str,input().split()))

    if query[0] == "1":
        heapq.heappush(balls,int(query[1]) - add)
    elif query[0] == "2":
        add += int(query[1])
    else:
        print(heapq.heappop(balls) + add)