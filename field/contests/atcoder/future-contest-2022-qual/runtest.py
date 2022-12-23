import subprocess

for i in range(30):
    cmd = 'cargo run --release --bin tester python a.py < C:\\Users\\otsuneko\\Documents\\GitHub\\competitive-programming\\tmp\\future-contest-2022-qual_a\\{}.txt > out.txt'.format(str(i).zfill(4))
    returncode = subprocess.run(cmd, shell=True, stdout = subprocess.PIPE)