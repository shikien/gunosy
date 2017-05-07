# gunosy

## 依存しているライブラリ
- MeCab
- pyquery

## サーバーの起動方法
```
cd infercat
python manage.py runserver
```

## 評価方法
alpha = 0.0001: 73.11%

alpha = 0.0010: 73.98%

alpha = 0.1000: 74.91%  // adopted

alpha = 1.0000: 73.78%

alpha = 10.0000: 52.93%
