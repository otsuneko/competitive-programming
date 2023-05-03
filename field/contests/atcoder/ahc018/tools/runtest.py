from re import sub
import subprocess
import time
import sys

# Rustのtester出力からスコア情報を抽出し保存するためのファイル
score_file_path = '/home/otsuneko/workspace/competitive-programming/field/contests/atcoder/ahc018/score.txt'
f = open(score_file_path, 'w')

# コマンドライン引数が与えられなければエラー
if len(sys.argv) < 2 or not sys.argv[1].isdecimal():
    print("実行するテストケースの数を入力してください")
    exit()

# li = [2,18,22,25,29,32,35,38,39,55,59,64,75,76]
li = [2,22,25,38,59,64,76]
# Rustのtester出力からスコア情報を抽出し書き出し
total = 0
for i in range(int(sys.argv[1])):
# for i in li:
    # start = time.time()
    cmd = "cargo run --release --bin tester pypy3 ../a.py < in/{0}.txt > out/{0}.txt".format(str(i).zfill(4))
    # end = time.time()
    returncode = subprocess.run(cmd, shell=True, capture_output=True,text=True)
    print(returncode.stderr)

    idx = returncode.stderr.find("Total Cost = ")
    score = returncode.stderr[idx+13:]
    f.write(score)
    # total += int(score)

    # print(score, end="")
    # print(end-start, score, end="")

# print(total)
f.close()