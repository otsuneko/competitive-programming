import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S1,S2,S3 = map(str,input().split())

if [S1,S2,S3] == ["<","<","<"]:
    print("B")
elif [S1,S2,S3] == ["<","<",">"]:
    print("C")
elif [S1,S2,S3] == ["<",">","<"]:
    print("A")
elif [S1,S2,S3] == ["<",">",">"]:
    print("A")
elif [S1,S2,S3] == [">","<","<"]:
    print("A")
elif [S1,S2,S3] == [">","<",">"]:
    print("A")
elif [S1,S2,S3] == [">",">","<"]:
    print("C")
elif [S1,S2,S3] == [">",">",">"]:
    print("B")
