# gunosy

## 概要
フォームから記事URLを受け取り、それをもとに記事カテゴリを判定する。

## 依存しているライブラリ
- MeCab
- pyquery

## サーバーの起動方法
```
cd infercat
python manage.py runserver
```

## 評価方法
交差検定を用いて、評価する。

alphaは正のパラメーターであり、以下のような正解率を得たので、実際には alpha = 0.1000 として実行した。

alpha = 0.0001: 73.11%

alpha = 0.0010: 73.98%

alpha = 0.1000: 74.91%  // adopted

alpha = 1.0000: 73.78%

alpha = 10.0000: 52.93%
