N = int(input())

login = []
for _ in range(N):
    A,B = map(int,input().split())
    login.append([A,1])
    login.append([A+B,-1])

login.sort()

ans = [0]*(N+1)
people = 0
start = login[0][0]
for log in login:
    cur,change = log

    if cur != start:
        ans[people] += cur-start
        start = cur

    people += change

print(*ans[1:])
