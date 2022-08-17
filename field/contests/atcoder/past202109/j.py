from collections import defaultdict
import bisect
N,Q = map(int,input().split())
A = [i for i in range(1,2*N+1)]

rot = defaultdict(bool)
for i in range(2*N):
    rot[i] = False
idxs = []
check = set()
for _ in range(Q):
    t,k = map(int,input().split())
    k -= 1
    # print(rot)

    if t == 1:
        if k >= N:
            k = 2*N-k-1
            idx = bisect.bisect_left(idxs,k)
            if idx >= len(idxs):
                idx = len(idxs)-1
            if rot[idxs[idx]]:
                print(A[2*N-k-1])
            else:
                print(A[k])
        else:
            idx = bisect.bisect_left(idxs,k)
            if idx >= len(idxs):
                idx = len(idxs)-1
            if rot[idxs[idx]] == False:
                print(A[2*N-k-1])
            else:
                print(A[k])

    else:
        if N-k-1 not in check:
            bisect.insort(idxs, N-k-1)
            check.add(N-k-1)
        idx = bisect.bisect_left(idxs, N-k-1)
        if idx >= len(idxs):
            idx = len(idxs)-1
        for i in range(idx-1,len(idxs)):
            rot[idxs[i]] = not rot[idxs[i]]