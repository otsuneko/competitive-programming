import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

def f(su):
    while su%2==0:
        su //= 2
    return su

N = int(input())
A = list(map(int,input().split()))

odd = []
even = []
for a in A:
    if a%2:
        odd.append(a)
    else:
        even.append(a)

ans = 0
su_even = sum(even)
for n in odd:
    ans += n*len(even) + su_even

print(ans)
print(odd,even)
