import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

from collections import deque

Sa = deque(input())
Sb = deque(input())
Sc = deque(input())

nxt = Sa.popleft()
while 1:
    match nxt:
        case "a":
            if not Sa:
                print("A")
                exit()
            nxt = Sa.popleft()
        case "b":
            if not Sb:
                print("B")
                exit()
            nxt = Sb.popleft()
        case "c":
            if not Sc:
                print("C")
                exit()
            nxt = Sc.popleft()
