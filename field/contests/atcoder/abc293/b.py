N = int(input())
A = list(map(int,input().split()))

s = set()
for i in range(N):
    if i not in s:
        s.add(A[i]-1)

al = set([i for i in range(N)])
s = sorted(list(al-s))

ans = []
for i in range(len(s)):
    ans.append(s[i]+1)
print(len(ans))
print(*ans)