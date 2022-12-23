from re import sub
import os
import subprocess

# 並列処理パラメータ
max_process = 1
proc_list = []

# 実行するテストケース数
N = 20

# テストケース実行
for i in range(N):
    if os.path.isfile("out\\{}.txt".format(str(i).zfill(4))):
        os.remove("out\\{}.txt".format(str(i).zfill(4)))

    cmd = "pypy3 a.py < in\\{}.txt >> out\\{}.txt".format(str(i).zfill(4),str(i).zfill(4))
    print(cmd)
    proc = subprocess.Popen(cmd,shell=True, stdout = subprocess.PIPE)
    proc_list.append(proc)
    if (i+1) % max_process == 0 or (i+1) == N:
        for subproc in proc_list:
            subproc.wait()
        proc_list = []


    if os.path.isfile("out\\out{}.txt"):
        os.remove("out\\out{}.txt".format(str(i).zfill(4)))

# スコア集計
if os.path.isfile("out.txt"):
    os.remove("out.txt")
with open("out.txt", mode='a') as fa:
    for i in range(N):
        with open('out\\{}.txt'.format(str(i).zfill(4)), mode='r') as fr:
            score = fr.read()
            fa.write(score)