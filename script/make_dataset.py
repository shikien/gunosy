import os, pickle
from itertools import islice
from scrape import extract_texts, extract_nouns, articles_of_category

if __name__ == '__main__':
  save_dir = '../dataset/'
  
  if os.path.exists('%snounid.pkl' % save_dir):
    with open('%snounid.pkl' % save_dir, 'rb') as f:
      nounid = pickle.load(f)
  else:
    nounid = {}
  
  for c in range(1, 9):
    for i, url in islice(enumerate(articles_of_category(c)), 0, 500):
      print('%d_%06d: %s' % (c, i, url))

      texts = extract_texts(url)
      nouns = extract_nouns(texts)
      
      ids = []
      for k, p in nouns:
        if k not in nounid:
          nounid[k] = len(nounid)
        ids.append((nounid[k], p))
      
      with open('%s%d_%06d.pkl' % (save_dir, c, i), 'wb') as f:
        pickle.dump(ids, f)

    with open('%snounid.pkl' % save_dir, 'wb') as f:
      pickle.dump(nounid, f)