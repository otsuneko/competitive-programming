#!/usr/bin/env python3
# from typing import *

MOD = 998244353

# def solve(N: str, M: str, a: List[str], b: List[str], c: List[str]) -> int:
def solve(N, M, a, b, c):
    pass  # TODO: edit here

# generated by oj-template v4.8.1 (https://github.com/online-judge-tools/template-generator)
def main():
    N, M = input().split()
    a = [None for _ in range(M)]
    b = [None for _ in range(M)]
    c = [None for _ in range(M)]
    for i in range(M):
        a[i], b[i], c[i] = input().split()
    a1 = solve(N, M, a, b, c)
    print(a1)

if __name__ == '__main__':
    main()
