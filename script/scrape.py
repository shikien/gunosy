from collections import defaultdict
from itertools import count
import MeCab
from pyquery import PyQuery as pq

def extract_texts(url):
  dom = pq(url)
  p = [pq(v) for v in dom('p')]
  return [v.text() for v in p if not v.children()]

def extract_nouns(texts):
  mcb = MeCab.Tagger()

  serial_nouns = []
  for text in texts:
    try:
      attrs = mcb.parse(text).split('\n')
      attrs = [v.split(',') for v in attrs if v and v != 'EOS']
      types = [v[0].split('\t')[1] for v in attrs]
      words = [v[6] for v in attrs]
      s = []
      for t, w in zip(types, words):
        if t == '名詞' and w != '*':
          s.append(w)
        else:
          serial_nouns.append(s)
          s = []
      serial_nouns.append(s)
    except:
      pass
  
  nouns = defaultdict(float)
  for s in serial_nouns:
    for k in range(1, len(s) + 1):
      for i in range(len(s) - k + 1):
        x = ''.join(s[i: i + k])
        nouns[x] += float(k) / len(s)
  return nouns.items()

# 1: エンタメ, 2: スポーツ, 3: おもしろ, 4: 国内, 5: 海外, 6: コラム, 7: IT・科学, 8: グルメ
def articles_of_category(c):
  for i in count(1):
    dom = pq('https://gunosy.com/categories/%d?page=%d' % (c, i))
    a = dom('div.list_title[data-role="article-title"] a')
    for v in a:
      yield pq(v).attr('href')

# test code
if __name__ == '__main__':
  url = articles_of_category(1).__next__()
  print(url)
  
  texts = extract_texts(url)
  nouns = extract_nouns(texts)
  print(nouns)