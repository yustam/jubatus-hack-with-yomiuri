#!/usr/bin/env python
# -*- coding: utf-8 -*-

host = 'ec2-54-64-214-12.ap-northeast-1.compute.amazonaws.com'
port = 9199
name = 'similar_article'

import jubatus, json, os, sys
import MeCab
from jubatus.recommender import client
from jubatus.recommender import types
from jubatus.common import Datum

import urllib2

recommender = client.Recommender(host, port, name)

url_prefix = 'http://www.yomiuri.co.jp/'
genre1_dic = {
    u'政治': 'politics',
    u'社会': 'national',
    u'経済': 'economy',
    u'スポーツ': 'sports',
    u'国際': 'world',
    u'地域': 'local',
    u'科学': 'science',
    u'カルチャー': 'culture',
    u'社説': 'editorial',
    u'環境': 'eco'
}
genre2_dic = {
    u'おくやみ': 'obit',
    u'プロ野球': 'sports/npb',
    u'高校野球本大会': 'sports/hsb/news02',
    u'大リーグ': 'sports/mlb',
    u'野球一般': 'sports/yakyu',
    u'サッカー': 'sports/soccer',
    u'ゴルフ': 'sports/golf',
    u'大相撲': 'sports/sumo',
    u'エトセトラ': 'sports/etc',
    u'五輪': 'sports/olympic',
    u'東京五輪': 'olympic/2020',
    u'高校総体': 'sports/interhigh',
    u'スポーツ特集': 'sports/special',
    u'写真特集': 'sports/photo',
    u'ウインタースポーツ': 'sports/winter',
    u'地方選': 'election/local',
    u'衆院選': 'election/shugiin',
    u'参院選': 'election/sangiin'
}
genre3_dic = {
    u'なでしこ': 'nadeshiko',
    u'国内': 'domestic',
    u'xxx': 'representative',
    u'海外': 'foreign'
}

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


train_data = []
article_data = open('data/articles2.json', 'r')
article_json = json.loads(article_data.read())
for article in article_json:
    try:
        title = ' '.join(article['HeadLine'])
        if title == '':
            continue
        if 'Genre1' not in article:
            continue
        genre1 = article['Genre1']
        genre2 = ''
        if 'Genre2' not in article:
            url = ''.join([url_prefix, genre1_dic[genre1], '/', article['DateId'][0], '-', article['NewsItemId'][0].split('-')[1], '.html'])
        else:
            genre2 = article['Genre2']
            if genre2 == u'サッカー':
                continue
            url = ''.join([url_prefix, genre2_dic[genre2], '/', article['DateId'][0], '-', article['NewsItemId'][0].split('-')[1], '.html'])
            # try:
            #     resp = urllib2.urlopen(url)
            # except urllib2.HTTPError, error:
            #     print('### ng ###')
        print(url)
        date = article['DateLine']
        article_text = ' '.join(article['article'])
        keywords = ' '.join(extractKeyword(article_text))
        datum = Datum({
            # "genre": ','.join([genre1, genre2]),
            "keywords": keywords,
            # "title": title,
            "date": date.replace('-','').replace(':','').replace(' ','')
        })
        # print(datum)
        recommender.update_row(url, datum)
    except:
        raise
        # print "Unexpected error:", sys.exc_info()[0]
