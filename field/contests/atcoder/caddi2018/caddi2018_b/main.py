#!/usr/bin/env python3
# from typing import *

FIRST = 'first'
SECOND = 'second'

# def solve(N: int, a: List[int]) -> str:
def solve(N, a):
    pass  # TODO: edit here

# generated by oj-template v4.8.1 (https://github.com/online-judge-tools/template-generator)
def main():
    N = int(input())
    a = [None for _ in range(N)]
    for i in range(N):
        a[i] = int(input())
    a1 = solve(N, a)
    print(a1)

if __name__ == '__main__':
    main()
