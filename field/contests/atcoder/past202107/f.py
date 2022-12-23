N = int(input())
timetable = [[] for _ in range(10**5+1)]
flag = False
for _ in range(N):
    D,S,T = map(int,input().split())

    for t in timetable[D]:
        if  max(t[0],S) < min(t[1],T):
            flag = True

    timetable[D].append([S,T])

print(["No","Yes"][flag])