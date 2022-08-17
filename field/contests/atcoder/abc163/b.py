N,M = map(int,input().split())
work = list(map(int,input().split()))
total = sum(work)
if N >= total:
    print(N-total)
else:
    print(-1)