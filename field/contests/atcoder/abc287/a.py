N = int(input())
S = [input() for _ in range(N)]


print(["No","Yes"][S.count("For") > N/2])
    