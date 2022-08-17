N,X,Y = map(int,input().split())
X,Y = X-1,Y-1

dic = dict()
for i in range(1,N):
    dic[i] = 0

for i in range(N):
    for j in range(i+1,N):
        k = 10**18
        k = min(k,j-i,abs(X-i) + abs(Y-j) + 1)
        dic[k] += 1

for key in dic:
    print(dic[key])

# original code
# N,X,Y = map(int,input().split())
# X,Y = X-1,Y-1
# graph = [[] for _ in range(N)]
# for i in range(N-1):
#   graph[i].append(i+1)
#   graph[i+1].append(i)

# graph[X].append(Y)
# graph[Y].append(X)

# dist1 = set()
# for s in range(N):
#     for to in graph[s]:
#         if s < to and (s,to) not in dist1:
#             dist1.add((s,to))

# print(len(dist1))

# nextdist = set(list(dist1))
# seen = set(list(dist1))
# for _ in range(N-2):
#     tmp = set()
#     for d in nextdist:
#         s = d[0]
#         t = d[1]
#         for ds in range(-1,2,2):
#             ns = s+ds
#             if ns < t and 0 <= ns < N and (ns,t) not in seen:
#                 tmp.add((ns,t))
#                 seen.add((ns,t))
#         for dt in range(-1,2,2):
#             nt = t+dt
#             if s < nt and 0 <= nt < N and (s,nt) not in seen:
#                 tmp.add((s,nt))
#                 seen.add((s,nt))

#     print(len(tmp))
#     nextdist = set(list(tmp))