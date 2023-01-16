import random
import sys

seed = random.seed(sys.argv[1])

print("50 2500")
for _ in range(50):
    print(*[random.randint(1, 9) for _ in range(50)])