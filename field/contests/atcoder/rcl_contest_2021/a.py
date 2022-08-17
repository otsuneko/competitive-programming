import bisect

def sort_with_index(arr):

    arr2 = sorted([ (x,i) for i, x in enumerate(arr)])
    val = []
    idx = []
    for i in range(len(arr2)):
        val.append(arr2[i][0])
        idx.append(arr2[i][1])

    return val,idx

N,M,K = map(int,input().split())
A = list(map(int,input().split()))

for _ in range(M):

    val,idx = sort_with_index(A)
    idx_receive = min(N-1, bisect.bisect(val,K))
    idx_give = min(N-1, bisect.bisect(val, K-val[idx_receive]+1))

    A[idx[idx_receive]] = (A[idx[idx_receive]] + A[idx[idx_give]])%K
    print(idx[idx_receive], idx[idx_give])
