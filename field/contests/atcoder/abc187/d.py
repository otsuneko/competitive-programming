from operator import itemgetter
N = int(input())
vote = []
total_a = 0
total_t = 0
for _ in range(N):
    A,B = map(int,input().split())
    vote.append([2*A+B,A,B])
    total_a += A

vote.sort(reverse=True,key=itemgetter(0))

ans = 0
for i in range(N):
    total_a -= vote[i][1]
    total_t += vote[i][1]+vote[i][2]
    ans += 1

    if total_t > total_a:
        break

print(ans)