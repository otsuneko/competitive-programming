from re import sub
import subprocess

for i in range(1):
    cmd = "cargo run --release --bin tester pypy3 a.py < too/in/{}.txt > tools/out/{}.txt".format(str(i).zfill(4),str(i).zfill(4))
    returncode = subprocess.run(cmd, shell=True, stdout = subprocess.PIPE)