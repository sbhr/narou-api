#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文字列のリスト（タイトル）が書かれたファイルを読み込み、
形態素解析して、単語と品詞のcsvで出力
"""

import csv
import os
import sys
import MeCab

# IPAの辞書
mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/ipadic')
# 多数のWeb上の言語資源から得た新語を追加することでカスタマイズした MeCab 用のシステム辞書
# mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
# バグ回避のため、事前に空文字をパース
mecab.parse('')


def morphological_analysis(text: str) -> [[str, str]]:
    """
    引数の文字列を形態素解析し、
    [[単語, 品詞]]のリストを返す
    """
    array = []
    node = mecab.parseToNode(text)

    while node:
        features = node.feature.split(",")
        try:
            # 単語によってはうまくパースできていないので、
            # 文字数バイト分を切り取る
            # 単語
            word = node.surface.encode()[:node.length].decode('utf-8')
            # うまく行く時こんな感じ
            # word = features[6] # ipadic
            # word = features[7] # unidic
        except:
            node = node.next
            continue
        # 品詞
        pos = features[0]
        if pos != 'BOS/EOS' and word != '':
            array.append([word, pos])
        node = node.next

    return array


if __name__ == '__main__':
    # ファイル名をコマンドライン引数で渡す
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

    output_file = 'words_{}.csv'.format(
        os.path.splitext(file_name)[0].split('_')[1])
    with open(output_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(result)
    f.close()
