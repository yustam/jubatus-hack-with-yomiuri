#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from jubatus.recommender import client
from jubatus.recommender import types
from jubatus.common import Datum

import lxml.html

host = 'ec2-54-64-214-12.ap-northeast-1.compute.amazonaws.com'
port = 9199
name = 'similar_article'

recommender = client.Recommender(host, port, name)

url = 'http://www.example.com/index.html'
datum = Datum({
    "keywords": '東京',
    "date": "20150822144300"
})
print(datum)
recommender.update_row(url, datum)

sr = recommender.similar_row_from_id(url, 5)
print(len(sr))
for item in sr:
    print item.score, item.id
    try:
        t = lxml.html.parse(item.id)
        print(t.find(".//title").text)
        print('---')
    except urllib2.HTTPError, error:
        print('### ng ###')
