N,M = map(int,input().split())
graph = [list(map(int,input().split())) for _ in range(N)]

import pypyjit
pypyjit.set_param('max_unroll_recursion=0')