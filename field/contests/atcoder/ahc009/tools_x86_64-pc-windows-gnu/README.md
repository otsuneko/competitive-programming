- [Usage](#usage)
  - [Requirements](#requirements)
  - [Input Generation](#input-generation)
  - [Visualization](#visualization)
- [使い方](#%E4%BD%BF%E3%81%84%E6%96%B9)
  - [実行環境](#%E5%AE%9F%E8%A1%8C%E7%92%B0%E5%A2%83)
  - [入力生成](#%E5%85%A5%E5%8A%9B%E7%94%9F%E6%88%90)
  - [ビジュアライザ](#%E3%83%93%E3%82%B8%E3%83%A5%E3%82%A2%E3%83%A9%E3%82%A4%E3%82%B6)

# Usage

## Requirements
Please install a compiler for Rust language (see https://www.rust-lang.org).
For those who are not familiar with the Rust language environment, we have prepared a [pre-compiled binary for Windows](https://img.atcoder.jp/ahc009/cf3f791aac0f80374c60_windows.zip).
The following examples assume that you will be working in the directory where this README is located.

## Input Generation
The `in` directory contains pre-generated input files for seed=0-99.
If you want more inputs, prepare `seeds.txt` which contains a list of random seeds (unsigned 64bit integers) and execute the following command.
```
cargo run --release --bin gen seeds.txt
```
When using the precompiled binary for Windows,
```
./gen.exe seeds.txt
```
This will output input files into `in` directory.

## Visualization
Let `in.txt` be an input file and `out.txt` be an output file.
You can visualize the output by executing the following command.
```
cargo run --release --bin vis in.txt out.txt
```
When using the precompiled binary for Windows,
```
./vis.exe in.txt out.txt
```

The above command writes a visualization result to `out.svg`.
It also outputs the score to standard output.
You can open the svg file using image viewers, web browsers, or via `vis.html` file.

You can also use a [web visualizer](https://img.atcoder.jp/ahc009/cf3f791aac0f80374c60.html?lang=en) which is more rich in features.
To use the web visualizer, copy and paste the output of your program into the Output filed of the visualizer.
By changing the number in the Seed field, you can switch to an input for another seed.
By pressing the `▶` button, animation will start.

# 使い方

## 実行環境
Rust言語のコンパイル環境が必要です。
https://www.rust-lang.org/ja を参考に各自インストールして下さい。
Rust言語の環境構築が面倒な方向けに、[Windows用のコンパイル済みバイナリ](https://img.atcoder.jp/ahc009/cf3f791aac0f80374c60_windows.zip)も用意してあります。
以下の実行例では、このREADMEが置かれているディレクトリに移動して作業することを想定しています。

## 入力生成
`in` ディレクトリに予め生成された seed=0~99 に対する入力ファイルが置かれています。
より多くの入力が欲しい場合は、`seeds.txt` に欲しい入力ファイルの数だけ乱数seed値(符号なし64bit整数値)を記入し、以下のコマンドを実行します。
```
cargo run --release --bin gen seeds.txt
```
Windows用のコンパイル済バイナリを使用する場合は以下のようにします。
```
./gen.exe seeds.txt
```

生成された入力ファイルは `in` ディレクトリに出力されます。


## ビジュアライザ
入力ファイル名を`in.txt`、出力ファイル名を`out.txt`としたとき、以下のコマンドを実行します。
```
cargo run --release --bin vis in.txt out.txt
```
Windows用のコンパイル済バイナリを使用する場合は以下のようにします。
```
./vis.exe in.txt out.txt
```

出力のビジュアライズ結果は `out.svg` というファイルに書き出されます。
標準出力にはスコアを出力します。
svgファイルは画像ビューアソフト、webブラウザなどで表示できます。
`vis.html` ファイルを開くことでも表示できます。

より機能が豊富な[ウェブ版のビジュアライザ](https://img.atcoder.jp/ahc009/cf3f791aac0f80374c60.html?lang=ja)も利用可能です。
ウェブ版のビジュアライザを使用するには、解答プログラムの出力をビジュアライザのOutput欄に貼り付けて下さい。
Seed欄の数字を変更することで他のseedの入力に切り替わります。
`▶` ボタンを押すとアニメーションが開始します。
