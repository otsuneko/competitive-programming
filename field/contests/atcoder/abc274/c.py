N = int(input())
A = list(map(int,input().split()))

ans = [0]*(2*N+2)

for i,a in enumerate(A):
    ans[(i+1)*2] = ans[(i+1)*2+1] = ans[a]+1

for a in ans[1:]:
    print(a)