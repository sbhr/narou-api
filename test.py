#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import gzip
import StringIO
import json

url = "http://api.syosetu.com/novelapi/api/"
query = u'無職転生　- 異世界行ったら本気だす -'
header = {
    'Accept-Encoding': "gzip,x-gzip,deflate,sdch,compress",
    'Accept-Content': 'gzip'
}
payload = {
    'gzip':'5',
    'out':'json',
    'isbl':'1'
    # 'title':'1',
    # 'word':query
}

# r = requests.get(url)
r = requests.get(url, params=payload)
print r.status_code
r.raw.decode_content = True;
# dat = zlib.decompress(r.text)
strIO = StringIO.StringIO(r.content)
dec = gzip.GzipFile(fileobj=strIO).read()
# gzip_file = gzip.GzipFile(fileobj=r.raw)
# r.encoding = 'utf-8'
# print dec
# print gzip_file.read()

f = open('data.json', 'w')
f.write(dec)
exit()

j = json.loads(dec)
for item in j:
    for i in item:
        print i,item[i]
