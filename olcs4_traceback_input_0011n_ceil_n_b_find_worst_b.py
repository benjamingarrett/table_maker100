# Usage: python analysis.py <folder_w_csv>


import csv, os, sys, matplotlib.pyplot as plt
from math import log, sqrt
import numpy as np
from scipy import stats


def get_list(fn):
  return [ln.rstrip('\n').split(',') for ln in open(fn)]


print('{}'.format(sys.argv))
fig = plt.figure()
ax = fig.add_subplot(111)
col = 1
files = [f for f in os.listdir(sys.argv[1]) if 'csv' in f]
k = 0
d = {}
while k < len(files):
  print('handling {}'.format(files[k][4:12]))
  tmp_str = files[k][15:]
  print('tmp_str-->{}<--'.format(tmp_str))
  b = int(tmp_str[0:tmp_str.find('.')])
  print('b={}'.format(b))
  d[b] = []
  lst = get_list(sys.argv[1]+'/'+files[k])
  j = 1
  while j < len(lst):
    d[b].append((int(lst[j][0]), int(lst[j][col])))
    j += 1
  k += 1
worst_b = {}
k = 0
n = 2
while n <= 1000:
  bmx = -1
  max_x = -1
  max_y = -1
  for b,lst in d.items():
    for pt in lst:
      if pt[0]==n:
        if pt[1] > max_y:
          max_x = pt[0]
          max_y = pt[1]
          bmx = b
  if bmx == -1:
    print('error: worst b not found')
    exit()
  worst_b[n] = (bmx, max_x, max_y)
  n += 1

categories = {}
for k,v in worst_b.items():
  if v[0] not in categories:
    categories[v[0]] = [(v[1], v[2])]
  else:
    categories[v[0]].append((v[1], v[2]))
for k,v in categories.items():
  x = [kk[0] for kk in v]
  y = [kk[1] for kk in v]
  ax.plot(x, y, label=k)



plt.xlabel('problem size (n)')
plt.ylabel('highest critical cache size')
ax.legend(loc='upper left')
t = 'OLCS v4 traceback, LRU, critical cache size'
t+= '\nInstance type: 0^a 1^a ... (b-1)^(n mod a), where a=ceiling(n/b)'
t+= '\nfor b in the range [1,14]'
t+= '\nPlot shows highest critical cache size for each b (when it is worst the b) for a given problem size'
plt.title(t)
plt.show()
