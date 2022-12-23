# N = int(input())
# first = ["",0]
# second = ["",0]
# for _ in range(N):
#     S,T = map(str,input().split())
#     if int(T) > first[1]:
#         second[0] = first[0]
#         second[1] = first[1]
#         first[0] = S
#         first[1] = int(T)
#     elif int(T) > second[1]:
#         second[0] = S
#         second[1] = int(T)
# print(second[0])

N = int(input())
mountain = []
for _ in range(N):
    name,height = map(str,input().split())
    height = int(height)
    mountain.append([name,height])

from operator import itemgetter
mountain.sort(key=itemgetter(1))
print(mountain[N-2][0])