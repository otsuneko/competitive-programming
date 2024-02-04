from re import sub
import subprocess

out = open("N_M_K.txt","w")

for i in range(100):
    f = open("tools/in/{}.txt".format(str(i).zfill(4)), 'r', encoding='UTF-8')

    nmk = f.readline()
    nmk = nmk.replace(" ",",")
    out.write(nmk[:5])
    out.write("\n")

    f.close()

out.close()