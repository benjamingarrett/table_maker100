# Usage: python analysis.py <folder_w_csv> <plot_#>
#   plot# in {1, 2, 3, 4, 5}


import os, sys, matplotlib.pyplot as plt
from math import floor, log, sqrt
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
  c = float(files[k][4:12])
  d[c] = []
  lst = get_list(sys.argv[1]+'/'+files[k])
  j = 1
  while j < len(lst):
    d[c].append((int(lst[j][0]), int(lst[j][col])))
    j += 1
  k += 1
worst_c = {}
k = 0
n = 2
while n <= 1000:
  cmx = -1
  mx = 0
  for c, lst in d.items():
    for pt in lst:
      if pt[0]==n:
        if pt[1] > mx:
          mx = pt[1]
          cmx = c
  if cmx == -1:
    print('error: worst c not found')
    exit()
  worst_c[n] = cmx
  n += 1

plot_number = int(sys.argv[2])
if plot_number == 1:
  pts = [(k, float(k**worst_c[k])) for k in sorted(worst_c.keys())]
  x = [k[0] for k in pts]
  y = [k[1] for k in pts]
  plt.xlabel('problem size (n)')
  plt.ylabel('n^c for c having highest critical cache size')
  ax.plot(x, y)
if plot_number == 2:
  pts = [(k, k/float(k**worst_c[k])) for k in sorted(worst_c.keys())]
  x = [k[0] for k in pts]
  y = [k[1] for k in pts]
  plt.xlabel('problem size (n)')
  plt.ylabel('n/n^c for c having highest critical cache size')
  ax.plot(x, y)
if plot_number == 3:
  pts = [(k, k/float(k**worst_c[k])) for k in sorted(worst_c.keys())]
  x = [k[0] for k in pts]
  y = [k[1] for k in pts]
  plt.xlabel('problem size log(n)')
  plt.ylabel('log(n/n^c) for c having highest critical cache size')
  ax.loglog(x, y, basex=2, basey=2)
if plot_number == 4:
  pts = [(k, k/float(k**worst_c[k])) for k in sorted(worst_c.keys())]
  x = [k[0] for k in pts]
  y = [k[1] for k in pts]
  plt.xlabel('problem size log(n)')
  plt.ylabel('n/n^c for c having highest critical cache size')
  ax.semilogx(x, y, basex=2)
if plot_number == 5:
  pts = [(k, k/float(k**worst_c[k])) for k in sorted(worst_c.keys())]
  x = [log(k[0], 2) for k in pts]
  y = [k[1] for k in pts]
  plt.xlabel('problem size log(log(n))')
  plt.ylabel('log(n/n^c) for c having highest critical cache size')
  ax.loglog(x, y, basex=2, basey=2)

t = 'OLCS v4 traceback, LRU, critical cache size'
t+= '\nInstance type: 0^a 1^a ... (b-1)^a b^(n-ab), where a=floor(n^c), b=floor(n/a)'
t+= '\nfor all c in the range (0,1) in increments of 0.01'
t+= '\nPlot shows worst a for a given problem size'
plt.title(t)
plt.show()


