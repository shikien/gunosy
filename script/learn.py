from math import log
from collections import defaultdict
import pickle
from nbm import NBM

def make_model_data(data_dir, indexes, alpha):
  lp = {} # lp[c][k] = log(the probability that the noun of id k appears in the category of id c)
  dv = {} # dv[c] = lp[c][unknown noun]
  for c in range(1, 9):
    s = defaultdict(float)
    for i in indexes:
      with open('%s%d_%06d.pkl' % (data_dir, c, i), 'rb') as f:
        ids = pickle.load(f)

      for k, p in ids:
        s[k] += p

    t = sum(s.values()) + len(s)
    dv[c] = log(alpha / t)
    lp[c] = {}
    for k, p in s.items():
      lp[c][k] = log((p + alpha) / t)

  return {'lp': lp, 'dv': dv}

def cross_validation(data_dir, indexes, n, alpha):
  k = int((len(indexes) + n - 1) / n)
  
  scs = []
  for z in range(n):
    test_indexes = indexes[z * k: (z + 1) * k]
    model_indexes = list(set(indexes) - set(test_indexes))

    model_data = make_model_data(data_dir, model_indexes, alpha)
    model = NBM(model_data, data_dir)

    s = 0
    for c in range(1, 9):
      for i in test_indexes:
        with open('%s%d_%06d.pkl' % (data_dir, c, i), 'rb') as f:
          ids = pickle.load(f)

        s += model.test(ids) == c
    
    scs.append(s / (len(test_indexes) * 9) * 100)

  return sum(scs) / len(scs)

if __name__ == '__main__':
  data_dir = '../dataset/'
  
  '''
  for alpha in [0.0001, 0.001, 0.1, 1, 10]:
    s = cross_validation(data_dir, list(range(500)), 5, alpha)
    print('alpha = %.4f: %.2f%%' % (alpha, s))
  '''

  model_data = make_model_data(data_dir, list(range(500)), 0.1)
  with open('../model/nbm.pkl', 'wb') as f:
    pickle.dump(model_data, f)

'''
alpha = 0.0001: 73.11%
alpha = 0.0010: 73.98%
alpha = 0.1000: 74.91%  // adopted
alpha = 1.0000: 73.78%
alpha = 10.0000: 52.93%
'''