#!/bin/bash
#online-judge-toolsでtmpに作成された一日以上前のファイルを削除する
#find /workspaces/atcoder/tmp/* -name graph_sample -prune -o -mtime -1 -exec echo {} \;
find /workspaces/atcoder/tmp/* -maxdepth 0 -name graph_sample -prune -o  -mtime +1 -exec rm -r {} \;