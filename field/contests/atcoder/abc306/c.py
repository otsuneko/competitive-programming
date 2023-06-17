N = int(input())
A = list(map(int,input().split()))

cnt = [0]*N
idx = [-1]*N
for i in range(3*N):
    cnt[A[i]-1] += 1
    if cnt[A[i]-1] == 2:
        idx[A[i]-1] = i+1

def sort_with_index(arr, reverse=False):
    if reverse:
        return sorted([ (x,i) for i, x in enumerate(arr)], reverse=True)
    else:
        return sorted([ (x,i+1) for i, x in enumerate(arr)])

tmp = sort_with_index(idx)
ans = []
for x,i in tmp:
    ans.append(i)
print(*ans)