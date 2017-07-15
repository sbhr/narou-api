#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文字列のリスト（タイトル）が書かれたファイルを読み込み、
形態素解析して、単語と品詞のcsvで出力
"""

import sys
import os
import csv
import MeCab

mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
mecab.parse('')


def morphological_analysis(text: str) -> [[str, str]]:
    """
    引数の文字列を形態素解析し、
    [[単語, 品詞]]のリストを返す
    """
    array = []
    node = mecab.parseToNode(text)

    while node:
        # 単語
        word = node.surface
        # 品詞
        pos = node.feature.split(",")[1]
        if word != '':
            array.append([word, pos])
        node = node.next

    return array


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('invalid arguments')
        sys.exit()

    file_path = sys.argv[1]
    file_name = os.path.basename(file_path)

    with open(file_path, 'r') as f:
        title_list = f.readlines()

    result = []
    for row in title_list:
        result.extend(morphological_analysis(row))
    f.close()

    output_file = 'words_{0}.csv'.format(
        os.path.splitext(file_name)[0].split('_')[1])
    with open(output_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(result)
    f.close()
