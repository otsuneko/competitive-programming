#!/usr/bin/env python3
# from typing import *

YES = 'Yes'
NO = 'No'

# def solve(N: int, M: int, A: List[int]) -> List[str]:
def solve(N, M, A):
    pass  # TODO: edit here

# generated by oj-template v4.8.1 (https://github.com/online-judge-tools/template-generator)
def main():
    import sys
    tokens = iter(sys.stdin.read().split())
    N = int(next(tokens))
    M = int(next(tokens))
    A = [None for _ in range(N)]
    for i in range(N):
        A[i] = int(next(tokens))
    assert next(tokens, None) is None
    ans = solve(N, M, A)
    for i in range(N):
        print(ans[i])

if __name__ == '__main__':
    main()
