#!/usr/bin/env python3
# from typing import *



# def solve(N: int, A: List[int], B: List[int]) -> List[str]:
def solve(N, A, B):
    login = []
    for i in range(N):
        login.append([A[i],1])
        login.append([A[i]+B[i],-1])

    login.sort()

    ans = [0]*(N+1)
    people = 0
    start = login[0][0]
    for log in login:
        cur,change = log

        if cur != start:
            ans[people] += cur-start
            start = cur

        people += change

    return ans[1:]

# generated by oj-template v4.8.1 (https://github.com/online-judge-tools/template-generator)
def main():
    N = int(input())
    A = [None for _ in range(N)]
    B = [None for _ in range(N)]
    for i in range(N):
        A[i], B[i] = map(int, input().split())
    D = solve(N, A, B)
    print(*[D[i] for i in range(N)])

if __name__ == '__main__':
    main()
