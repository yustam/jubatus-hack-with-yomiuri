# jubatus-hack-with-yomiuri

8/22~23に開催された`Jubatus Hackathon with 読売新聞`の成果物です。
レコメンドのチュートリアルを応用して記事レコメンドを作成し実際に利用できる形にしてみました。

## 仕組み

![仕組み](image.png?raw=true "image")

## ソースの説明

- data/
 - 今回提供された学習データ(読売新聞オンラインの記事572件)
- extension/
 - レコメンドを表示するChrome拡張機能
- analyze.py
 - Jubatusのレコメンドを確認するクライアント(テスト用)
- api.py
 - Chrome拡張機能とJubatusサーバを中継するAPI
 - 拡張機能から渡されたURLをスクレイプしてキーワードを抽出後Jubatusに類似記事をレコメンドさせる
- similar_article.json
 - Jubatusサーバの設定ファイル。ほぼチュートリアル通り。
- train_yomiuri.py
 - 読売新聞オンラインの記事データをJubatusサーバに学習させるためのクライアント
 - 記事データJSON -> 元記事URL復元/本文からキーワード抽出 -> Jubatusに食わせる

## 動かし方

### Jubatus Server

Jubatusインストール済みのAMI(jubatus-0.8.1:ami-0c34b20c)を使用しました(公式？)
(publicなので`jubatus`で検索すれば出てくる)
`ubuntu`なのでubuntuユーザでログインして`similar_article.json`で起動
ポートはデフォルトの9199番を使用。

```bash
jubarecommender --configpath similar_article.json
```

### API Server

こちらは通常のAmazon Linuxを使用。jubatusクライアントやMeCabをインストールする。
Flaskを使用している。依存ライブラリをインストールしたら下記コマンドで起動。
ポートはデフォルトの5000番を使用。

```bash
python api.py
```

### 学習

Jubatusサーバに記事データを投入する。
こちらはMacクライアントで実行した。brew/pipでほぼ必要な物は全て入る。
(jubatus,mecab,mecab-pythonなど)
インストールしたら下記コマンドで実行。

```bash
python train_yomiuri.py
```

### APIのテスト

外部からアクセス可能か試してみる。
パラメータにURLを渡すとJubatusの学習データの中からキーワードに類似した記事を3件返す。
URLと一緒に返すスコアが1に近いほど類似度が高い。

```bash
$ curl http://{ホスト名}:5000/?url=http://www.example.com/
{
  "articles": [
    {
      "score": 0.08671099692583084,
      "title": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
      "url": "http://www.yomiuri.co.jp/world/20150819-OYT1T50109.html"
    },
    {
      "score": 0.07412493228912354,
      "title": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
      "url": "http://www.yomiuri.co.jp/economy/20150812-OYT1T50003.html"
    },
    {
      "score": 0.0678844228386879,
      "title": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
      "url": "http://www.yomiuri.co.jp/national/20150816-OYT1T50053.html"
    }
  ],
  "keywords": [
    "Snippets",
    "datetime",
    "Python"
  ]
}
```

### Chrome拡張

`extension`ディレクトリごと拡張機能としてChromeに設定する
あとはpublicアクセス可能な任意のページで拡張機能を開くとレコメンドが表示される

## 参考URL

普段pythonをあまり触っていないので色々と参考にさせていただきました。Flask便利。

- API Server
 - http://d.hatena.ne.jp/chronogazer/20130327/1364400376
 - http://qiita.com/ShingoOikawa/items/175be8a472ec8ed8a707
 - http://blog.mwsoft.jp/article/57078793.html

- Chrome Extension
 - http://qiita.com/suin/items/2b31079056f1356257cb
 - http://placehold.jp/
 - http://qiita.com/5a3i/items/a031427727e4923005d0
 - http://stackoverflow.com/questions/2797853/get-url-and-save-it-chrome-extension
