import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
P =  [list(map(int,input().split())) for _ in range(N)]

# class Prob:
#     def __init__(self, num, denom):
#         self.numerator = num
#         self.denominator = denom

#     def __lt__(self, other):
#         return self.denominator * other.numerator < self.numerator * other.denominator

li = []
for i in range(N):
    # li.append((Prob(P[i][0], P[i][0] + P[i][1]), i+1))
    li.append((P[i][0] * 10**19 // (P[i][0] + P[i][1]), i+1))

li.sort(key = lambda x:(-x[0],x[1]))

ans = []
for s in li:
    ans.append(s[1])

print(*ans)