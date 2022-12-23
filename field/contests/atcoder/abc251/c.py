from collections import defaultdict
dict = defaultdict(int)

N =int(input())
poem = []
for i in range(N):
    s,t =map(str,input().split())
    if dict[s] == 0:
        dict[s] += 1
        poem.append((int(t),s,i+1))

poem.sort(key=lambda x:(-x[0],x[2]))
print(poem[0][2])
