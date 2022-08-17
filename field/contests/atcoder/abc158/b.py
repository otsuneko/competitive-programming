N,A,B = map(int,input().split())

cnt = N//(A+B)
print(A*cnt + min(A,N-(A+B)*cnt))
