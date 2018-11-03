#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
なろうAPIからジャンルを選択して、
総合評価順に全て（最大2000件）のタイトルを取得する
"""

import datetime
import gzip
import json
import requests

API_URL = "http://api.syosetu.com/novelapi/api/"

GENRE_TXT = """
    ジャンル一覧
    101: 異世界〔恋愛〕
    102: 現実世界〔恋愛〕
    201: ハイファンタジー〔ファンタジー〕
    202: ローファンタジー〔ファンタジー〕
    301: 純文学〔文芸〕
    302: ヒューマンドラマ〔文芸〕
    303: 歴史〔文芸〕
    304: 推理〔文芸〕
    305: ホラー〔文芸〕
    306: アクション〔文芸〕
    307: コメディー〔文芸〕
    401: VRゲーム〔SF〕
    402: 宇宙〔SF〕
    403: 空想科学〔SF〕
    404: パニック〔SF〕
    9901: 童話〔その他〕
    9902: 詩〔その他〕
    9903: エッセイ〔その他〕
    9904: リプレイ〔その他〕
    9999: その他〔その他〕
    9801: ノンジャンル〔ノンジャンル〕
"""
GENRE_LIST = [
    '101', '102',
    '201', '202', '301', '302', '303', '304', '305', '306', '307',
    '401', '402', '403', '404',
    '9901', '9902', '9903', '9904', '9999', '9801'
]


def make_params(param={}) -> dict:
    """
    必須パラメータを含めたなろうAPI用パラメータを返す
    """
    params = dict(
        gzip=5,
        out='json'
    )
    if len(param) > 0:
        params.update(param)
    return params


def get_narou_data(params: dict) -> [dict]:
    """
    引数のパラメータを用いてAPIを叩いてJsonデータに整形して返す
    """
    r = requests.get(API_URL, params=params)
    if r.status_code != 200:
        print('Faild to request')
        exit()
    return json.loads(gzip.decompress(r.content).decode('utf-8'))


def get_allcount(params: dict) -> int:
    """
    引数のパラメータに当てはまる総データ数を返す
    """
    data = get_narou_data(params)
    return data[0]['allcount']


def get_narou_data_until_max(params: dict, max: int):
    """
    max（最大2000）件までデータを取得する
    """
    data = []
    count = 0
    LIMIT = 500

    params.update({'lim': LIMIT})
    if max > 2000:
        max = 2000

    while max - count > 0:
        print('{0}%'.format(round(count/max*100)))
        params.update({'st': count + 1})
        temp = get_narou_data(params)
        del temp[0]  # delete allcount
        data.extend(temp)
        count += LIMIT
    print('100%')

    return data


print(GENRE_TXT)
print('ジャンルの番号を入力してください ', end='')
genre = input()
while genre not in GENRE_LIST:
    print('番号が異なります ', end='')
    genre = input()

params = make_params({'of': 't', 'genre': genre, 'order': 'hyoka'})
allcount = get_allcount(params)
data = get_narou_data_until_max(params, allcount)

f = open('title_{}_{}.txt'.format(genre, datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")), 'w')
for item in data:
    f.write(item['title'] + '\n')
f.close()
