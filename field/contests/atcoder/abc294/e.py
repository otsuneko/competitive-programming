def count_same_elements(A2, B2):
    n = len(A2)
    m = len(B2)
    same_count = 0
    i,pre_i = 0,-1
    j,pre_j = 0,-1
    total_a_len = total_b_len = 0
    while i < n and j < m:
        # print(i,j,total_a_len, total_b_len, same_count)
        a_val,a_len = A2[i]
        b_val,b_len = B2[j]
        if pre_i != i:
            pre_total_a_len = total_a_len
            total_a_len += a_len
        if pre_j != j:
            pre_total_b_len = total_b_len
            total_b_len += b_len
        pre_i = i
        pre_j = j

        if total_a_len == total_b_len:
            if a_val == b_val:
                same_count += min(a_len,b_len)
            i += 1
            j += 1
        elif total_a_len < total_b_len:
            if a_val == b_val:
                if pre_total_a_len >= pre_total_b_len:
                    same_count += total_a_len - pre_total_a_len
                else:
                    same_count += total_a_len - pre_total_b_len
            i += 1
        elif total_a_len > total_b_len:
            if a_val == b_val:
                if pre_total_b_len >= pre_total_a_len:
                    same_count += total_b_len - pre_total_b_len
                else:
                    same_count += total_b_len - pre_total_a_len
            j += 1
    return same_count

# def count_same_elements(A2, B2):
#     n = len(A2)
#     same_count = 0
#     i = 0
#     j = 0
#     for k in range(n):
#         a_len, a_val = A2[k]
#         b_len, b_val = B2[k]
#         if a_val == b_val and i == j:
#             same_count += min(a_len, b_len)
#         i += a_len
#         j += b_len
#     return same_count

L,N1,N2 = map(int,input().split())

A2 = [list(map(int,input().split())) for _ in range(N1)]
B2 = [list(map(int,input().split())) for _ in range(N2)]

print(count_same_elements(A2,B2))