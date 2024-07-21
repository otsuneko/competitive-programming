import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

def nth_palindrome(n):
    length = 1
    count = 9
    total = 0

    while total + count < n:
        total += count
        length += 1
        if length % 2 == 0:
            count = 9 * (10 ** (length // 2 - 1))
        else:
            count = 9 * (10 ** (length // 2))

    pos = n - total - 1
    if length % 2 == 0:
        half = 10 ** (length // 2 - 1) + pos
        return int(str(half) + str(half)[::-1])
    else:
        half = 10 ** (length // 2) + pos
        return int(str(half) + str(half)[-2::-1])

N = int(input())
print(nth_palindrome(N-1))
