from collections import Counter
def nCr(n, r):

    res = 1
    for i in range(r):
        res = (res*(n-i))//(i+1)

    return res

N = int(input())
A = list(map(int,input().split()))
count = Counter(A)
li = sorted([key for key in count])

ans = 0
for i in range(len(li)):
    for j in range(i+1,len(li)):
        ans += (li[i]-li[j])**2 * count[li[i]] * count[li[j]]
print(ans)