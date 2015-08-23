# -*- coding: utf-8 -*-

import json

from flask import Flask, request, jsonify

import sys, datetime
from jubatus.recommender import client
from jubatus.recommender import types
from jubatus.common import Datum

import lxml.html
from urlparse import urljoin
import MeCab

app = Flask(__name__)

host = 'ec2-54-64-214-12.ap-northeast-1.compute.amazonaws.com'
port = 9199
name = 'similar_article'

def extractKeyword(text):
    tagger = MeCab.Tagger()
    encoded_text = text.encode('utf-8')
    node = tagger.parseToNode(encoded_text).next
    keywords1 = [] # 固有名詞 地域
    keywords2 = [] # 固有名詞 人名
    keywords3 = [] # 固有名詞 組織
    keywords4 = [] # 一般名詞
    while node:
        if node.feature.split(",")[0] == "名詞":
            if node.feature.split(",")[1] == "固有名詞":
                if node.feature.split(",")[2] == "地域":
                    keywords1.append(node.surface)
                elif node.feature.split(",")[2] == "人名":
                    keywords2.append(node.surface)
                elif node.feature.split(",")[2] == "組織":
                    keywords3.append(node.surface)
            if node.feature.split(",")[1] == "一般":
                keywords4.append(node.surface)
        node = node.next
    keywords1.extend(keywords2)
    keywords1.extend(keywords3)
    keywords1.extend(keywords4)
    return keywords1

@app.route("/")
def hello():
    recommender = client.Recommender(host, port, name)
    url = request.args.get('url', 'http://www.example.com/')
    t = lxml.html.parse(url)
    keywords = extractKeyword(t.find(".//title").text.replace(u'読売新聞（YOMIURI ONLINE）',''))
    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    print(date)
    print(','.join(keywords))
    datum = Datum({
        "keywords": ' '.join(keywords),
        "date": date
    })
    recommender.update_row(url, datum)
    sr = recommender.similar_row_from_id(url, 4)
    data = []
    for item in sr:
        t2 = lxml.html.parse(item.id)
        data.append({"score":item.score, "url":item.id, "title":t2.find(".//title").text})
    data.pop(0)
    return jsonify(keywords=keywords,articles=data)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
