@echo off
setlocal enabledelayedexpansion
for /l %%a in (0,1,30) do (
  set num=000%%a
  set num=!num:~-4,4!
  echo !num!
  cargo run --release --bin tester pypy a.py < C:\\Users\\otsuneko\\Documents\\GitHub\\competitive-programming\\tmp\\future-contest-2022-qual_a\\!num!.txt > out.txt
)
endlocal