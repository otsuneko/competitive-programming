import sys
import subprocess
args = sys.argv

if not (args[1] and args[2]):
    print("enter a contest and problem name(e.g. abc147 e).")
    exit()

contest_name = args[1]
problem_name = args[2]

# rustファイル作成
subprocess.run("w3m \"https://atcoder.jp/contests/{0}/submissions?f.Task={0}_{1}&f.LanguageName=Rust&f.Status=AC&f.User=\"".format(contest_name, problem_name), shell=True)