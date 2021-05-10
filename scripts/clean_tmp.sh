#!/bin/bash
#online-judge-toolsでtmpに作成された一日以上前のファイルを削除する
dir_name="$(cd $(dirname $0); pwd)"
dir_name=${dir_name\\scripts}

#find $dir_name/tmp/* -name graph_sample -prune -o -mtime -1 -exec echo {} \;
find $dir_name\\tmp\\* -maxdepth 0 -name graph_sample -prune -o  -mtime +1 -exec rm -r {} \;