# Usage: python analysis.py <folder_w_csv> <plot#> <b> <max_x>
# n,csize,misses
# plot 1: csize
# plot 2: running max
# plot 3: csize multiples of 60
# plot 4: running max, multiples of 60


import csv, os, sys, matplotlib.pyplot as plt
from math import log, sqrt, floor
import numpy as np
from scipy import stats


def get_list(fn):
  return [ln.rstrip('\n').split(',') for ln in open(fn)]


print('{}'.format(sys.argv))
plot_type = int(sys.argv[2])
chosen_b = int(sys.argv[3])
largest_x = int(sys.argv[4])
fig = plt.figure()
ax = fig.add_subplot(111)
col = 1
files = [f for f in os.listdir(sys.argv[1]) if 'csv' in f]
k = 0
d = {}
max_xx = 0
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
    xx = int(lst[j][0])
    if xx > largest_x:
      j = len(lst)
    else:
      max_xx = xx if xx > max_xx else max_xx
      d[b].append((int(lst[j][0]), int(lst[j][col])))
      j += 1
  k += 1
if plot_type == 1:
  for k,v in d.items():
    x = [p[0] for p in v]
    y = [p[1] for p in v]
    if chosen_b == -1:
      ax.plot(x, y, '*', label='b={}'.format(k))
    elif chosen_b == k:
      ax.plot(x, y, '*', label='b={}'.format(k))
  plt.xlabel('problem size (n)')
  plt.ylabel('critical cache size')
  t = 'OLCS v4 traceback, LRU, critical cache size'
  t+= '\nInstance type: a = ceiling(n/b)'
  t+= '\n1st sequence: 0^a 1^a ... (b-1)^(n-(b-1)a)'
  t+= '\n2nd sequence: (b-1)^(n-(b-1)a) 1^a 0^a'
  ax.legend(loc='upper left')
  plt.title(t)
  plt.show()
  exit()
if plot_type == 2:
  for k,v in d.items():
    x, y = [v[0][0]], [v[0][1]]
    for p in v:
      x.append(p[0])
      if p[1] > y[-1]:
        y.append(p[1])
      else:
        y.append(y[-1])
    if chosen_b == -1:
      ax.plot(x, y, '*', label=k)
    elif chosen_b == k:
      ax.plot(x, y, '*', label=k)
  plt.xlabel('problem size (n)')
  plt.ylabel('running max of critical cache size')
  t = 'OLCS v4 traceback, LRU, critical cache size'
  t+= '\nInstance type: a = ceiling(n/b)'
  t+= '\n1st sequence: 0^a 1^a ... (b-1)^(n-(b-1)a)'
  t+= '\n2nd sequence: (b-1)^(n-(b-1)a) 1^a 0^a'
  t+= '\nRunning max'
  ax.legend(loc='upper left')
  plt.title(t)
  plt.show()
  exit()
if plot_type == 3:
  for k,v in d.items():
    x = [p[0] for p in v if floor(p[0]/60)-p[0]/60==0]
    y = [p[1] for p in v if floor(p[0]/60)-p[0]/60==0]
    if chosen_b == -1:
      ax.plot(x, y, '*', label=k)
    elif chosen_b == k:
      ax.plot(x, y, '*', label=k)
  plt.xlabel('problem size (n)')
  plt.ylabel('critical cache size')
  t = 'OLCS v4 traceback, LRU, critical cache size'
  t+= '\nInstance type: a = ceiling(n/b)'
  t+= '\n1st sequence: 0^a 1^a ... (b-1)^(n-(b-1)a)'
  t+= '\n2nd sequence: (b-1)^(n-(b-1)a) 1^a 0^a'
  t+= '\nConsidering only multiples of 60'
  ax.legend(loc='upper left')
  plt.title(t)
  plt.show()
  exit()
if plot_type == 4:
  for k,v in d.items():
    x, y = [v[0][0]], [v[0][1]]
    for p in v:
      if floor(p[0]/60)-p[0]/60==0:
        x.append(p[0])
        if p[1] > y[-1]:
          y.append(p[1])
        else:
          y.append(y[-1])
    if chosen_b == -1:
      ax.plot(x, y, '*', label=k)
    elif chosen_b == k:
      ax.plot(x, y, '*', label=k)
  plt.xlabel('problem size (n)')
  plt.ylabel('running max of critical cache size')
  t = 'OLCS v4 traceback, LRU, critical cache size'
  t+= '\nInstance type: a = ceiling(n/b)'
  t+= '\n1st sequence: 0^a 1^a ... (b-1)^(n-(b-1)a)'
  t+= '\n2nd sequence: (b-1)^(n-(b-1)a) 1^a 0^a'
  t+= '\nRunning max, considering only multiples of 60'
  ax.legend(loc='upper left')
  plt.title(t)
  plt.show()
  exit()



# disregard below

worst_b = {}
k = 0
n = 2
print('b values {}'.format(d.keys()))
while n <= max_xx:
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
#print('worst_b keys {}'.format(worst_b.keys()))
categories = {}
for k,v in worst_b.items():
  if v[0] not in categories:
    categories[v[0]] = [(v[1], v[2])]
  else:
    categories[v[0]].append((v[1], v[2]))
print('categories {}'.format(categories.keys()))
for k,v in categories.items():
  x = [kk[0] for kk in v]
  y = [kk[1] for kk in v]
  ax.plot(x, y, '*', label=k)



plt.xlabel('problem size (n)')
plt.ylabel('highest critical cache size')
t = 'OLCS v4 traceback, LRU, critical cache size'
t+= '\nInstance type: 0^a 1^a ... (b-1)^(n mod a), where a=ceiling(n/b)'
t+= '\nfor b in the range [1,14]'
t+= '\nPlot shows highest critical cache size for each b (when it is worst the b) for a given problem size'


ax.legend(loc='upper left')
plt.title(t)
plt.show()
