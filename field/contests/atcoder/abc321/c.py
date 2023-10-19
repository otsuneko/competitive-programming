import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

K = int(input())

li = [[] for _ in range(10)]
li[0] = [i for i in range(10)]

ans = [i for i in range(10)]
for digit in range(1,10):
    for n in li[digit-1]:
        n = str(n)
        for i in range(10):
            if int(n[-1]) <= i:
                break
            li[digit].append(n + str(i))
            ans.append(n + str(i))

print(ans[K])