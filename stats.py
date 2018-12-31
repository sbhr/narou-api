#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
改行区切りに値読み込み
最大値や平均値などの統計値を出力する

入力ファイル例
1
2
3
4
...
"""
import sys
import statistics

def trim(str):
    return int(str.replace('\n', '').replace('\r', ''))

# ファイル読み込み
args = sys.argv
f = open(args[1], "r")

# 改行ごとに区切ってリストにする
lines = f.readlines()
l = list(map(trim, lines))

# 標準出力に
# 最大値、最小値、平均値、中央値、最頻値、標準偏差、分散
# を出力
print('{0},{1},{2},{3},{4},{5},{6}'.format(max(l),min(l),round(statistics.mean(l),2),statistics.median(l),statistics.mode(l),round(statistics.stdev(l),2),round(statistics.variance(l),2)))
