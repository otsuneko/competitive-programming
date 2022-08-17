# Pythonで提出！！
import sys
sys.setrecursionlimit(10**7)

def dfs(s,li):
    
    if len(li) >= 10**2:
        return

    if s == 5:
        txt = "".join([c for c in li if c != "E"])
        print("".join(li))
        if txt == txt[::-1]:
            print("".join(li))
            exit()

    for to,chr in graph[s]:
        if li[-4:] != ["B","E","B","E"] and li[-4:] != ["A","E","A","E"] and li[-4:] != ["A","E","C","E"] and li[-4:] != ["A","E","E","B"] and li[-4:] != ["C","E","C","E"] and li[-4:] != ["D","B","E","B"]:
            li.append(chr)
            dfs(to,li)
            li.pop()

N,M = 10,15
graph = [[] for _ in range(N)]
graph[0].append((2,"D"))
graph[1].append((2,"E"))
graph[1].append((6,"D"))
graph[2].append((1,"B"))
graph[2].append((1,"C"))
graph[2].append((3,"E"))
graph[3].append((4,"A"))
graph[4].append((1,"E"))
graph[6].append((7,"A"))
graph[6].append((7,"C"))
graph[6].append((9,"E"))
graph[7].append((6,"E"))
graph[7].append((5,"D"))
graph[8].append((7,"E"))
graph[9].append((8,"B"))

dfs(0,[])

DBDEBED