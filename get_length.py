#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
改行ごとに文字列を区切り、文字列長を出力する

入力ファイル例

吾輩は猫である
羅生門
伊豆の踊り子
堕落論
"""
import sys

def length(str):
    return len(str)

args = sys.argv
num = args[1].split('_')[1]

f = open(args[1], "r")
lines = f.readlines()

lengths = list(map(length, lines))

for row in lengths:
    print(row)

f.close()

