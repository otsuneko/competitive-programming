from re import sub
import subprocess
import time
import sys
import os

# Rustのtester出力からスコア情報を抽出し保存するためのファイル
score_file_path = os.getcwd() + '/../score.txt'
f = open(score_file_path, 'w')

# コマンドライン引数が与えられなければエラー
if len(sys.argv) < 2 or not sys.argv[1].isdecimal():
    print("実行するテストケースの数を入力してください")
    exit()

li_lt9 = [3,10,13,30,34,41]
li_gt9 = [12,18,23,29,30,36]
li_gt25 = [0,7,11,16,17,20,42,43,49]
li_gt100 = [9,14,47,48,51,63,71,81,83,85]
li_gt200 = [1,22,27,31,32,39,50,54]
li_gt300 = [2,15,21,28,38]
li_gt500 = [4,5,19,35,45,46]
li_gt750 = [6,8,24,25,26,33,40,44]

# Rustのtester出力からスコア情報を抽出し書き出し
total_score = 0
for i in range(int(sys.argv[1])):
# for i in li_gt750:
    start = time.time()
    cmd = "cargo run --release --bin tester pypy3 ../a.py < in/{0}.txt > out/{0}.txt".format(str(i).zfill(4))
    returncode = subprocess.run(cmd, shell=True, capture_output=True,text=True)
    end = time.time()
    print("{0}.txt".format(str(i).zfill(4)))
    print(returncode.stderr, end="")

    # 標準エラー出力を改行文字で分割して、各行をリストに格納
    stderr_lines = returncode.stderr.split('\n')

    # ★★★★★ここを問題に応じて書き換える★★★★★
    target_string = "Score = "
    
    # 特定の文字列を含む行を抜き出す
    matching_lines = [line for line in stderr_lines if target_string in line]
    
    if matching_lines:
        for line in matching_lines:
            score = line.replace(target_string, "")
            f.write(score)
            f.write("\n")

            total_score += int(score)

    print("Duration time:", end-start)
    print()

f.write(str(total_score))
print(total_score)
f.close()