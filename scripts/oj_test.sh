#!/bin/bash
file=$1
echo $file

dir_name="$(cd $(dirname $0); pwd)"
dir_name=${dir_name//scripts/}

file_name="${file##*/}"
file_name="${file_name%.*}"

folder_name="${file%/*}"
folder_name="${folder_name##*/}"
echo "$dir_name,$file_name,$folder_name"
#otherの問題の場合
if [ $folder_name = 'other_problems' ]; then
#echo $file_name
#abc160_a_問題名.pyといった問題名とする
folder_name=${file_name%%'_'*}
file_name=$(echo ${file_name} | sed -e 's/[^_]*\_\([^_]*\)$/\1/')
echo "$folder_name,${file_name}"
fi

#echo "file,folder,$file_name,$folder_name"
problem_id="${folder_name}_${file_name}"

#atcoder/testにsampleが無ければディレクトリ生成、ダウンロード
md=${dir_name}tmp/${problem_id}

if [ ! -e $md ]; then
    echo "dir not exist. make:$md"
    mkdir $md
fi
if [ -z "$(ls $md)" ]; then    
    oj_url="https://atcoder.jp/contests/$folder_name/tasks/$problem_id"
    oj d $oj_url --format "$md/sample-%i.%e"
fi

#sampleに対するテストを実行
oj t -c "python $1" -d "${dir_name}tmp/${problem_id}"