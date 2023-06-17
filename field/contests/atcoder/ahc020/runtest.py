from re import sub
import subprocess

for i in range(100):
    cmd = "pypy3 a.py < tools/in/{}.txt > tools/out/{}.txt".format(str(i).zfill(4),str(i).zfill(4))
    returncode = subprocess.run(cmd, shell=True, stdout = subprocess.PIPE)