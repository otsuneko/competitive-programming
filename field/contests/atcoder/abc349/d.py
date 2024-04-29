import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

L, R = map(int, input().split())
ans = []
# LがRを追い越さない限り、Lが約数に持つ最大の2^iをLに足していく
while L < R:
    i = 0
    # Lが2で割り切れる限り&2^iをLに足した時にRを追い越さない限り2で割り続ける
    while L%pow(2,i+1) == 0 and L + pow(2,i+1) <= R:
        i += 1
    ans.append((L,L+pow(2,i)))
    L += pow(2,i)

print(len(ans))
for a in ans:
    print(*a)
