# ・調和級数を忘れていた(二重ループに見えても、jがiずつ増えていくときはNlogNでいける)
# ・約数の分布を表に書いて、式の通りの数え方以外に別の数え方が無いか考えるべき(横のカウント→縦のカウント)

N = int(input())
fx = [0]*(N+1)

for i in range(1,N+1):
  j = i
  while j <= N:
    fx[j] += 1
    j += i

ans = 0
for i in range(1,N+1):
  ans += i * fx[i]

print(ans)


# ### maspy-san's answer (O(N**0.5)) ###
# N = int(input())

# def f(x):
#   return x * (x+1) // 2
 
# ans = 0
# for x in range(1, N+1):
#   if x * x > N:
#     break
#   # x = y
#   ans += x * x
#   # x < y の 2 倍
#   y_high = N//x
#   ans += 2 * x * (f(y_high) - f(x))
 
# print(ans)

# ### kanpurin-san's answer (O(N**0.5)) ###
# # N = int(input())

# # ans = 0
# # for i in range(1,N+1):
# #     if i**2 <= N:
# #         mul_sum = (1+N//i)*(N//i)//2
# #         ans += i * mul_sum
# #     else:
# #         break
# # if i > 1:
# #     for k in range(1,N//(i-1)):
# #         mul_sum = k*(1+k)//2
# #         ans += (N//k - N//(k+1)) * (1 + N//k + N//(k+1)) // 2 * mul_sum
    
# # print(ans)


# ### original code (O(N)) ###
# # N = int(input())
# # ans = 0
# # for i in range(1,N+1):
# #     mul_sum = (1+N//i)*(N//i)//2
# #     ans += i*mul_sum
# # print(ans)