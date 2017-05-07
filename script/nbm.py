from collections import defaultdict
import pickle
from scrape import extract_texts, extract_nouns

class NBM:
  def __init__(self, model_data, data_dir):
    with open('%snounid.pkl' % data_dir, 'rb') as f:
      self._nounid = defaultdict(lambda: -1, pickle.load(f))

    self._lp = {}
    for c, x in model_data['lp'].items():
      self._lp[c] = defaultdict(lambda: model_data['dv'][c], x)

  def test(self, ids):
    cp = defaultdict(float)
    for c in range(1, 9):
      for k, p in ids:
        cp[c] += self._lp[c][k] * p
    
    m = max(cp.values())
    for c, v in cp.items():
      if v == m:
        return c

  def calc(self, url):
    texts = extract_texts(url)
    nouns = extract_nouns(texts)
    ids = [(self._nounid[k], p) for k, p in nouns]
    c = self.test(ids)
    return {1: 'エンタメ', 2: 'スポーツ', 3: 'おもしろ', 4: '国内', 5: '海外', 6: 'コラム', 7: 'IT・科学', 8: 'グルメ'}[c]