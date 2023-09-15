from re import sub
import subprocess

out = open("L_N_S.txt","w")

for i in range(100):
    f = open("tools/in/{}.txt".format(str(i).zfill(4)), 'r', encoding='UTF-8')

    L_N_S = f.readline().rstrip()
    li = L_N_S.split(" ")

    out.write(",".join(li))
    out.write("\n")

    f.close()

out.close()