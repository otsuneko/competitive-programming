
N = int(input())
A = list(map(int,input().split()))

def add(i, x):
    while i <= N:
        data[i] += x
        i += i & -i
def get(i):
    s = 0
    while i:
        s += data[i]
        i -= i & -i
    return s
 
inv = [0]*N
for x in range(N):
    ans = 0
    A2 = A[x:]
    data = [0]*(len(A2)+1)
    for a in A2:
        add(a, 1)
        ans += a-get(a)
    inv[x] = ans
 
print(inv)