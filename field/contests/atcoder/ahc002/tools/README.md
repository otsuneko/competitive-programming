# Usage

## Requirements
Please install a compiler for Rust language (see https://www.rust-lang.org).

## Input Generation
Prepare `seeds.txt` which contains a list of random seeds (unsigned 64bit integers) and execute the following command.
```
cargo run --release --bin gen seeds.txt
```

This will output input files into `in` directory.

## Visualization
Let `in.txt` be an input file and `out.txt` be an output file.
You can visualize the output by executing the following command.
```
cargo run --release --bin vis in.txt out.txt
```
The above command writes a visualization result to `out.svg`.
It also outputs the score to standard output.
You can open the svg file using image viewers, web browsers, or via `vis.html` file.

# 使い方

## 実行環境
Rust言語のコンパイル環境が必要です。
https://www.rust-lang.org/ja を参考に各自インストールして下さい。

## 入力生成
`seeds.txt` に欲しい入力ファイルの数だけ乱数seed値(符号なし64bit整数値)を記入し、以下のコマンドを実行します。
```
cargo run --release --bin gen seeds.txt
```

生成された入力ファイルは `in` ディレクトリに出力されます。

## ビジュアライザ
入力ファイル名を`in.txt`、出力ファイル名を`out.txt`としたとき、以下のコマンドを実行します。
```
cargo run --release --bin vis in.txt out.txt
```
出力のビジュアライズ結果は `out.svg` というファイルに書き出されます。
標準出力にはスコアを出力します。
svgファイルは画像ビューアソフト、webブラウザなどで表示できます。
`vis.html` ファイルを開くことでも表示できます。
